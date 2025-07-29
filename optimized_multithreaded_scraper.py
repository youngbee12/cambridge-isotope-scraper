#!/usr/bin/env python3
"""
优化的多线程Cambridge Isotope Laboratories爬虫
改进了数据提取和404页面处理
"""

import time
import json
import re
import csv
import random
import threading
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
from datetime import datetime
import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OptimizedMultithreadedScraper:
    def __init__(self, max_workers=2, headless=True):
        self.max_workers = max_workers
        self.headless = headless
        self.products = []
        self.failed_urls = []
        self.skipped_urls = []
        self.lock = threading.Lock()
        self.output_prefix = 'optimized_products'
        
        # 设置Chrome选项
        self.chrome_options = Options()
        if self.headless:
            self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # 快速检查session
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
    def create_driver(self):
        """为每个线程创建独立的WebDriver实例"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                service = Service(ChromeDriverManager().install())

                # 为高线程数添加额外的Chrome选项
                options = Options()
                for arg in self.chrome_options.arguments:
                    options.add_argument(arg)

                # 高线程数时的额外优化
                if self.max_workers > 8:
                    options.add_argument("--disable-extensions")
                    options.add_argument("--disable-plugins")
                    options.add_argument("--disable-images")
                    options.add_argument("--disable-javascript")  # 可能影响数据提取
                    options.add_argument("--memory-pressure-off")
                    options.add_argument("--max_old_space_size=4096")

                driver = webdriver.Chrome(service=service, options=options)
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                driver.set_page_load_timeout(30)
                return driver

            except Exception as e:
                logger.warning(f"创建WebDriver失败 (尝试 {attempt+1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(random.uniform(1, 3))  # 随机延迟后重试
    
    def quick_check_page_status(self, url):
        """快速检查页面状态"""
        try:
            response = self.session.head(url, timeout=5, allow_redirects=True)
            if response.status_code == 404:
                return 'not_found'
            elif response.status_code >= 400:
                return 'error'
            elif response.status_code == 200:
                return 'ok'
            else:
                return 'unknown'
        except:
            return 'unknown'
    
    def extract_product_info_optimized(self, url):
        """优化的产品信息提取"""
        thread_id = threading.current_thread().ident
        logger.info(f"[线程{thread_id}] 处理: {url}")
        
        # 快速检查页面状态
        status = self.quick_check_page_status(url)
        if status == 'not_found':
            logger.info(f"[线程{thread_id}] 快速跳过404页面: {url}")
            with self.lock:
                self.skipped_urls.append(url)
            return None
        
        driver = self.create_driver()
        
        try:
            # 根据线程数动态调整延迟
            if self.max_workers > 16:
                initial_delay = random.uniform(8, 15)  # 高线程数时更长延迟
            elif self.max_workers > 8:
                initial_delay = random.uniform(5, 10)
            else:
                initial_delay = random.uniform(3, 6)

            driver.get(url)
            time.sleep(initial_delay)

            # 等待页面完全加载
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

            # 等待React/JavaScript内容加载
            time.sleep(8)  # 增加等待时间让动态内容加载

            # 尝试等待特定元素出现
            try:
                WebDriverWait(driver, 10).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".Details_customHorizontal")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".Details_customVertical")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
                    )
                )
                time.sleep(3)  # 额外等待确保内容完全加载
            except TimeoutException:
                logger.warning(f"[线程{thread_id}] 等待页面元素超时，继续尝试提取")
            
            # 检查404页面
            page_title = driver.title.lower()
            if 'not found' in page_title or 'page cannot be found' in page_title:
                logger.info(f"[线程{thread_id}] Selenium检测到404页面: {url}")
                with self.lock:
                    self.skipped_urls.append(url)
                return None
            
            product_info = {
                'url': url,
                'name': '',
                'product_number': '',
                'cas_labeled': '',
                'cas_unlabeled': '',
                'synonyms': '',
                'formula': '',
                'molecular_weight': '',
                'isotopic_enrichment': '',
                'chemical_purity': '',
                'description': '',
                'image_url': '',
                'page_title': driver.title
            }
            
            # 提取基本信息
            product_info['name'] = self.extract_product_name(driver)
            product_info['product_number'] = self.extract_product_number(url)
            product_info['image_url'] = self.extract_product_image(driver)
            
            # 等待动态内容加载
            time.sleep(2)
            
            # 提取详细信息 - 使用多种方法
            self.extract_details_comprehensive(driver, product_info)

            # 调试信息：显示页面内容
            logger.info(f"[线程{thread_id}] 页面标题: {driver.title}")
            logger.info(f"[线程{thread_id}] 页面URL: {driver.current_url}")

            # 检查页面是否包含产品详情元素
            details_elements = driver.find_elements(By.CSS_SELECTOR, ".Details_customHorizontal, .Details_customVertical")
            logger.info(f"[线程{thread_id}] 找到 {len(details_elements)} 个详情元素")

            # 验证提取结果
            if product_info['name'] or product_info['cas_labeled'] or product_info['formula']:
                logger.info(f"[线程{thread_id}] ✅ 成功提取: {product_info['name']} ({product_info['product_number']})")
                logger.info(f"[线程{thread_id}]   CAS: {product_info['cas_labeled']} / {product_info['cas_unlabeled']}")
                logger.info(f"[线程{thread_id}]   分子式: {product_info['formula']}")
                return product_info
            else:
                logger.warning(f"[线程{thread_id}] ⚠️  提取的数据为空: {url}")
                logger.warning(f"[线程{thread_id}]   页面标题: {driver.title}")

                # 保存页面源码用于调试
                try:
                    with open(f'debug_page_{thread_id}_{int(time.time())}.html', 'w', encoding='utf-8') as f:
                        f.write(driver.page_source)
                    logger.info(f"[线程{thread_id}] 页面源码已保存用于调试")
                except:
                    pass

                return product_info  # 仍然返回，即使数据为空
            
        except Exception as e:
            logger.error(f"[线程{thread_id}] 提取失败 {url}: {e}")
            with self.lock:
                self.failed_urls.append(url)
            return None
        
        finally:
            driver.quit()
    
    def extract_product_name(self, driver):
        """提取产品名称"""
        name_selectors = [
            'h1',
            '.product-title',
            '.product-name',
            '.page-title',
            '.entry-title',
            '[data-testid="product-name"]'
        ]
        
        for selector in name_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and len(text) > 3 and 'Cambridge Isotope' not in text and 'not found' not in text.lower():
                        return text
            except:
                continue
        
        # 从页面标题提取
        try:
            title = driver.title
            if title and 'Cambridge Isotope' in title and 'not found' not in title.lower():
                # 提取产品名称部分
                name_match = re.search(r'^([^-]+)', title)
                if name_match:
                    name = name_match.group(1).strip()
                    if len(name) > 3:
                        return name
        except:
            pass
        
        return ''
    
    def extract_product_number(self, url):
        """从URL提取产品编号"""
        patterns = [
            r'([cdno]lm-\d+(?:-[a-z0-9]+)?)',
            r'itemno=([A-Z0-9-]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url, re.IGNORECASE)
            if match:
                return match.group(1).upper()
        
        return ''
    
    def extract_product_image(self, driver):
        """提取产品图片URL"""
        try:
            # 等待图片加载
            time.sleep(1)
            
            image_selectors = [
                'img[src*="/product/image/"]',
                'img[src*="cdlm-"]',
                'img[src*="clm-"]',
                'img[src*="dlm-"]',
                'img[src*="nlm-"]',
                'img[src*="olm-"]',
                '.product-image img',
                '.product-photo img'
            ]
            
            for selector in image_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        src = element.get_attribute('src')
                        if src and '/product/image/' in src:
                            if src.startswith('/'):
                                src = 'https://isotope.com' + src
                            return src
                except:
                    continue
        except:
            pass
        
        return ''
    
    def extract_details_comprehensive(self, driver, product_info):
        """综合提取详细信息"""
        try:
            # 方法1: CSS选择器提取
            self.extract_details_by_css(driver, product_info)
            
            # 方法2: 如果CSS方法没有获取到主要信息，使用页面源码提取
            if not product_info['cas_labeled'] and not product_info['cas_unlabeled']:
                self.extract_details_from_source(driver, product_info)
            
            # 方法3: 尝试等待并重新提取
            if not product_info['cas_labeled'] and not product_info['formula']:
                time.sleep(2)
                self.extract_details_by_css(driver, product_info)
        
        except Exception as e:
            logger.warning(f"详细信息提取失败: {e}")
    
    def extract_details_by_css(self, driver, product_info):
        """使用CSS选择器提取详细信息"""
        thread_id = threading.current_thread().ident
        extracted_count = 0

        try:
            detail_selectors = ['.Details_customHorizontal', '.Details_customVertical']

            for selector in detail_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    logger.info(f"[线程{thread_id}] 找到 {len(elements)} 个 {selector} 元素")

                    for i, element in enumerate(elements):
                        try:
                            name_element = element.find_element(By.CSS_SELECTOR, '.Details_name')
                            name = name_element.text.strip().lower()

                            spans = element.find_elements(By.TAG_NAME, 'span')
                            if len(spans) >= 2:
                                value = spans[1].text.strip()
                                logger.info(f"[线程{thread_id}] 元素{i}: '{name}' = '{value}'")

                                if 'cas number labeled' in name:
                                    product_info['cas_labeled'] = value
                                    extracted_count += 1
                                elif 'cas number unlabeled' in name:
                                    product_info['cas_unlabeled'] = value
                                    extracted_count += 1
                                elif 'formula' in name:
                                    product_info['formula'] = value
                                    extracted_count += 1
                                elif 'synonyms' in name and not product_info['synonyms']:
                                    product_info['synonyms'] = value
                                    extracted_count += 1
                                elif 'molecular weight' in name:
                                    product_info['molecular_weight'] = value
                                    extracted_count += 1
                                elif 'enrichment' in name:
                                    product_info['isotopic_enrichment'] = value
                                    extracted_count += 1
                                elif 'purity' in name:
                                    product_info['chemical_purity'] = value
                                    extracted_count += 1
                            else:
                                logger.warning(f"[线程{thread_id}] 元素{i}没有足够的span: {len(spans)}")
                        except Exception as e:
                            logger.warning(f"[线程{thread_id}] 处理元素{i}失败: {e}")
                            continue
                except Exception as e:
                    logger.warning(f"[线程{thread_id}] 查找{selector}失败: {e}")
                    continue

            logger.info(f"[线程{thread_id}] CSS提取完成，共提取 {extracted_count} 个字段")

        except Exception as e:
            logger.error(f"[线程{thread_id}] CSS提取总体失败: {e}")
    
    def extract_details_from_source(self, driver, product_info):
        """从页面源码提取详细信息"""
        try:
            page_source = driver.page_source
            
            # CAS号提取
            cas_patterns = [
                (r'>CAS Number Labeled</span><span>(\d{1,7}-\d{2}-\d)</span>', 'labeled'),
                (r'>CAS Number Unlabeled</span><span>(\d{1,7}-\d{2}-\d)</span>', 'unlabeled'),
                (r'CAS\s*Number\s*Labeled[:\s]*(\d{1,7}-\d{2}-\d)', 'labeled'),
                (r'CAS\s*Number\s*Unlabeled[:\s]*(\d{1,7}-\d{2}-\d)', 'unlabeled'),
            ]
            
            for pattern, cas_type in cas_patterns:
                matches = re.findall(pattern, page_source, re.IGNORECASE)
                if matches:
                    if cas_type == 'labeled':
                        product_info['cas_labeled'] = matches[0]
                    elif cas_type == 'unlabeled':
                        product_info['cas_unlabeled'] = matches[0]
            
            # 分子式提取
            formula_patterns = [
                r'>Formula</span><span>([^<]+)</span>',
                r'Formula[:\s]*([A-Z][a-z]?(?:\d+)?(?:[A-Z*][a-z]?(?:\d+)?)*)',
            ]
            
            for pattern in formula_patterns:
                matches = re.findall(pattern, page_source, re.IGNORECASE)
                if matches:
                    product_info['formula'] = matches[0].strip()
                    break
        except:
            pass
    
    def scrape_products_multithreaded(self, urls, max_products=None):
        """多线程爬取产品"""
        if max_products:
            urls = urls[:max_products]
        
        logger.info(f"开始多线程爬取 {len(urls)} 个产品，使用 {self.max_workers} 个线程")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {executor.submit(self.extract_product_info_optimized, url): url for url in urls}
            
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    if result:
                        with self.lock:
                            self.products.append(result)
                            logger.info(f"进度: {len(self.products)} 个产品已完成")
                except Exception as e:
                    logger.error(f"处理 {url} 时出错: {e}")
                    with self.lock:
                        self.failed_urls.append(url)
        
        logger.info(f"多线程爬取完成！")
        logger.info(f"成功: {len(self.products)} 个")
        logger.info(f"跳过: {len(self.skipped_urls)} 个")
        logger.info(f"失败: {len(self.failed_urls)} 个")
    
    def save_results(self):
        """保存结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if self.products:
            # 保存为CSV
            csv_filename = f'{self.output_prefix}_{timestamp}.csv'
            df = pd.DataFrame(self.products)
            df.to_csv(csv_filename, index=False, encoding='utf-8')
            logger.info(f"CSV文件已保存: {csv_filename}")

            # 保存为Excel
            excel_filename = f'{self.output_prefix}_{timestamp}.xlsx'
            df.to_excel(excel_filename, index=False, engine='openpyxl')
            logger.info(f"Excel文件已保存: {excel_filename}")
        
        # 保存跳过和失败的URL
        if self.skipped_urls:
            with open(f'skipped_urls_{timestamp}.txt', 'w', encoding='utf-8') as f:
                for url in self.skipped_urls:
                    f.write(url + '\n')
        
        if self.failed_urls:
            with open(f'failed_urls_{timestamp}.txt', 'w', encoding='utf-8') as f:
                for url in self.failed_urls:
                    f.write(url + '\n')
        
        # 显示统计信息
        print(f"\n=== 优化多线程爬取结果 ===")
        print(f"总处理数量: {len(self.products) + len(self.skipped_urls) + len(self.failed_urls)}")
        print(f"成功获取: {len(self.products)}")
        print(f"跳过404页面: {len(self.skipped_urls)}")
        print(f"失败: {len(self.failed_urls)}")
        
        if self.products:
            df = pd.DataFrame(self.products)
            print(f"\n数据质量:")
            print(f"有产品名称: {len(df[df['name'] != ''])}")
            print(f"有CAS Labeled: {len(df[df['cas_labeled'] != ''])}")
            print(f"有CAS Unlabeled: {len(df[df['cas_unlabeled'] != ''])}")
            print(f"有分子式: {len(df[df['formula'] != ''])}")
            print(f"有图片: {len(df[df['image_url'] != ''])}")
            
            return csv_filename, excel_filename
        
        return None, None

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='Cambridge Isotope Laboratories 多线程爬虫')

    parser.add_argument('-t', '--threads', type=int, default=2,
                       help='线程数量 (默认: 2, 建议: 2-8, 最大: 128)')

    parser.add_argument('-n', '--max-products', type=int, default=None,
                       help='最大爬取产品数量 (默认: 无限制)')

    parser.add_argument('--headless', action='store_true',
                       help='使用headless模式 (默认: False)')

    parser.add_argument('-u', '--urls-file', type=str, default=None,
                       help='包含URL列表的文件路径 (默认: 使用内置测试URL)')

    parser.add_argument('-o', '--output-prefix', type=str, default='optimized_products',
                       help='输出文件前缀 (默认: optimized_products)')

    parser.add_argument('-v', '--verbose', action='store_true',
                       help='详细输出模式')

    return parser.parse_args()

def load_urls_from_file(file_path):
    """从文件加载URL列表"""
    urls = []
    try:
        if file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    # 如果是URL字符串列表
                    if all(isinstance(item, str) for item in data):
                        urls = data
                    # 如果是包含URL的对象列表
                    else:
                        urls = [item.get('url', '') for item in data if item.get('url')]
        else:
            # 文本文件，每行一个URL
            with open(file_path, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]

        logger.info(f"从文件 {file_path} 加载了 {len(urls)} 个URL")
        return urls

    except Exception as e:
        logger.error(f"加载URL文件失败: {e}")
        return []

def main():
    """主函数"""
    args = parse_arguments()

    # 验证线程数并给出警告
    if args.threads > 16:
        print(f"⚠️  警告: 使用 {args.threads} 个线程可能导致以下问题:")
        print(f"   - 网站可能封禁您的IP地址")
        print(f"   - 系统资源消耗过大 (预计需要 {args.threads * 200}MB+ 内存)")
        print(f"   - 可能被视为DDoS攻击")

        if args.threads > 64:
            print(f"❌ 强烈不建议使用超过64个线程!")
            response = input("是否继续? (输入 'yes' 继续): ")
            if response.lower() != 'yes':
                print("已取消执行")
                return

    elif args.threads > 8:
        print(f"⚠️  注意: {args.threads} 个线程较多，建议监控系统资源使用情况")

    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    print(f"\n=== Cambridge Isotope Laboratories 多线程爬虫 ===")
    print(f"线程数: {args.threads}")
    print(f"Headless模式: {args.headless}")
    print(f"最大产品数: {args.max_products or '无限制'}")
    print(f"输出前缀: {args.output_prefix}")

    # 获取URL列表
    if args.urls_file:
        urls = load_urls_from_file(args.urls_file)
        if not urls:
            print("错误: 无法从文件加载URL")
            return
    else:
        # 使用内置测试URL
        urls = [
            "https://isotope.com/carbohydrates/d-glucose-1-13c-6-13c-6-6-d2-cdlm-4895",
            "https://isotope.com/minimal-media-reagents/d-glucose-u-13c6-clm-1396-1",
            "https://isotope.com/dimethyl-sulfoxide-d6-dlm-10-10",
            "https://isotope.com/amino-acids/free-amino-acids/l-alanine-1-13c-clm-116-pk",
            "https://isotope.com/chloroform-d-dlm-7-10",  # 404
            "https://isotope.com/methanol-d4-dlm-24-10",  # 404
        ]
        print(f"使用内置测试URL: {len(urls)} 个")

    # 创建爬虫实例
    scraper = OptimizedMultithreadedScraper(
        max_workers=args.threads,
        headless=args.headless
    )

    # 设置输出前缀
    scraper.output_prefix = args.output_prefix

    try:
        print(f"\n开始爬取...")
        scraper.scrape_products_multithreaded(urls, max_products=args.max_products)
        csv_file, excel_file = scraper.save_results()

        if csv_file:
            print(f"\n✅ 多线程爬取完成！")
            print(f"📁 文件已保存:")
            print(f"   - {csv_file}")
            print(f"   - {excel_file}")
        else:
            print(f"\n⚠️  没有成功爬取到数据")

    except KeyboardInterrupt:
        print(f"\n⏹️  用户中断了爬取过程")
        scraper.save_results()
    except Exception as e:
        print(f"\n❌ 爬取过程出错: {e}")
        scraper.save_results()

if __name__ == "__main__":
    main()
