import os
import re
from rich.console import Console
from openai import Client

console = Console()

class RidgesGenerator:
    """
    Adapter for Ridges (Subnet 62) - Secure Automation Generation.
    Generates Selenium/Puppeteer code that bypasses ADA v2 detection.
    """
    def __init__(self):
        # We use Targon or Chutes as the underlying LLM for generation, 
        # acting as the "Ridges" subnet intelligence.
        self.api_key = os.getenv("TARGON_API_KEY") or os.getenv("CHUTES_API_KEY")
        self.base_url = "https://api.targon.com/v1" if os.getenv("TARGON_API_KEY") else "https://llm.chutes.ai/v1"
        self.model = os.getenv("RIDGES_MODEL", "deepseek-ai/DeepSeek-V3") # capable coder
        
        if self.api_key:
            self.client = Client(api_key=self.api_key, base_url=self.base_url)
        else:
            self.client = None

    def generate_script(self, url: str, instruction: str) -> str:
        """
        Generates a secure Selenium script for the given URL and instruction.
        Enforces ADA v2 compliance.
        """
        console.print(f"[magenta]🛠️ Ridges (SN62): Generating secure script for {url}...[/magenta]")
        
        prompt = f"""
        You are an expert in browser automation and anti-detection techniques.
        Generate a complete Python Selenium script to:
        1. Navigate to: {url}
        2. Perform action: {instruction}
        3. Print the result/content to stdout.

        CRITICAL SECURITY REQUIREMENTS (ADA v2 Protocol):
        - DO NOT use default Selenium webdriver.Chrome().
        - You MUST use `undetected_chromedriver` or standard selenium with specific flags.
        - You MUST inject the following arguments to ChromeOptions:
          - `--disable-blink-features=AutomationControlled`
          - `--no-sandbox`
          - `--disable-dev-shm-usage`
        - You MUST use `Page.addScriptToEvaluateOnNewDocument` to:
          - Mask `navigator.webdriver` (set to undefined).
          - Simulate `deviceMemory` = 8.
          - Simulate `hardwareConcurrency` = 16.
          - Set user agent to a recent Chrome version.
        
        Output ONLY the Python code block. No markdown, no explanations.
        """
        
        if not self.client:
            return self._mock_generation(url)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000
            )
            code = response.choices[0].message.content
            # Strip markdown fence if present
            code = re.sub(r"```python\n|```", "", code)
            return code
        except Exception as e:
            console.print(f"[red]Ridges Generation Failed: {e}[/red]")
            return self._mock_generation(url)

    def _mock_generation(self, url):
        return f"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
# ADA v2 Countermeasures
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1280,1024')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)

# Mask navigator.webdriver and Hardware Simulation (ADA v2)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {{
    "source": \"\"\"
    Object.defineProperty(navigator, 'webdriver', {{ get: () => undefined }});
    Object.defineProperty(navigator, 'deviceMemory', {{ get: () => 8 }});
    Object.defineProperty(navigator, 'hardwareConcurrency', {{ get: () => 16 }});
    \"\"\"
}})

driver.get("{url}")
print(driver.title)
driver.quit()
"""
