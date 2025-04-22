# XMLRPC & WPLOGIN Bruteforce + Auto Upload

This tool is designed for security researchers and penetration testers to test the security of WordPress websites. It attempts to brute-force login credentials using both the wp-login.php and xmlrpc.php methods and, upon successful login, uploads a specified plugin and/or theme.

**Disclaimer:** This tool is for **educational and authorized testing purposes only**. Unauthorized use on systems you do not own or have permission to test is illegal and unethical. The author is not responsible for any misuse or damage caused by this tool.

## Features
- Asynchronous bruteforce with `asyncio` + `httpx`
- Supports login via `wp-login.php` and `xmlrpc.php`
- Checks if a target website is a WordPress site.
- Brute-forces login credentials using a provided password list with various transformations.
- Uploads a specified plugin and/or theme upon successful login.
- Verifies the uploaded plugin or theme by checking for specific strings.
- Loads local OpenSSL DLLs on Windows for SSL compatibility.
- Bypasses SSL verification for flexibility in testing environments.

## Requirements

- Python 3.7 or higher
- Required Python libraries:
  - `httpx`
  - `colorama`
  - `requests`
  - `asyncio`
  - `ssl`
  - `ctypes` (for Windows users)

You can install the required libraries using pip:

```bash
pip install httpx colorama requests
```

## Usage

1. **Prepare the target list file:** Create a text file containing the list of target websites, one per line. For example:

   ```
   http://example.com
   http://anotherexample.com
   ```

2. **Prepare the password list file:** Create a text file containing the list of passwords to try. The tool supports placeholders in the passwords that will be replaced with transformations of the username and domain. For example:

   ```
   [WPLOGIN]123
   password[DOMAIN]
   [YEAR]admin
   ```

   Available placeholders:

   - `[WPLOGIN]`: Replaced with the username.
   - `[UPPERLOGIN]`: Replaced with the username in uppercase.
   - `[DOMAIN]`: Replaced with the domain name without the TLD.
   - `[DDOMAIN]`: Replaced with the full domain name.
   - `[YEAR]`: Replaced with the current year.
   - `[UPPERALL]`: Replaced with the username in uppercase.
   - `[LOWERALL]`: Replaced with the username in lowercase.
   - `[UPPERONE]`: Replaced with the username capitalized.
   - `[LOWERONE]`: Replaced with the first letter lowercase and the rest uppercase.
   - `[AZDOMAIN]`: Replaced with the domain name without special characters.
   - `[REVERSE]`: Replaced with the reversed username.
   - `[DVERSE]`: Replaced with the reversed domain name without TLD.
   - `[UPPERDO]`: Replaced with the domain name capitalized without TLD.
   - `[UPPERDOMAIN]`: Replaced with the full domain name in uppercase.

3. **Prepare the plugin and theme zip files:** The tool looks for `plugin-inmymine.zip` and `theme-inmymine.zip` in the same directory as the script. These should be the zip files you want to upload upon successful login.

4. **Run the script:** Execute the script using Python:

   ```bash
   python main.py
   ```

   You will be prompted to enter the path to the target list file and the password list file.

5. **Output:** The tool will output the results to the console and save successful logins to `success.txt`. If uploads fail, the site will be logged in `failed.txt`. Uploaded plugins and themes will be saved in `plugins.txt` and `themes.txt`, respectively.

## example
```bash
[INFO] OpenSSL Version: OpenSSL 1.1.1
Enter target list file: x.txt
Enter password list file: password.txt
[found username] http://example.com: ['admin']
[FAIL] http://example.com -> admin:password123
[SUCCESS] http://example.com -> admin:admin2025
[UPLOAD SUCCESS] Plugin: http://example.com/wp-content/plugins/random123/install.php
```
## How It Works

1. **WordPress Detection:** The tool checks if the target site has a `wp-login.php` page and looks for specific strings to confirm it's a WordPress site.
2. **Username Enumeration:** It attempts to retrieve usernames from the WordPress REST API endpoint `/wp-json/wp/v2/users`. Falls back to default username (admin) if enumeration fails
3. **Brute-Force Login:** For each username, it tries each password in the list, applying transformations based on the placeholders. It attempts to log in using both the wp-login.php and xmlrpc.php methods.
4. **Upload Plugin/Theme:** Upon successful login, it uploads the specified plugin and/or theme zip files using the WordPress admin interface.
5. **Verification:** It checks if the uploaded plugin or theme is active by verifying specific strings in the response from the uploaded file's URL.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.

1. Fork this repository.
2. Create a pull request with your changes.
3. Report bugs or suggestions via GitHub issues.

## License

This project is licensed under the MIT License.

## Contact

For any inquiries, you can reach me at:

- GitHub: InMyMine7
- Telegram: t.me/minsepen

---

**Note:** This tool is for educational and testing purposes only. Always ensure you have permission before testing any website.