import requests

# Define proxy dict. Don't forget to put your real user and pass here as well.
proxies = {
  "http": "http://CUWYAETQ6JCGF3CPO09I4403NJFRQL2JEQ73Y1JCQXWEK8C6OQHLLPIXJ0EPYENX7UPDEULM7W6E0YIM:render_js=False&premium_proxy=True@proxy.scrapingbee.com:8886"
  # 'https': 'http://kanan:8UZ8*u*p9tVNhri@unblock.oxylabs.io:60000',
}

response = requests.request(
    'GET',
    'http://flight724.com',
    verify=False,  # Ignore the certificate
    proxies=proxies,
)

# Print result page to stdout
print(response.text)

# Save returned HTML to result.html file
# with open('result.html', 'w') as f:
#     f.write(response.text)