import requests
from bs4 import BeautifulSoup

# Function to clean IPO names based on known endings (IPO or SME)
def clean_ipo_name(name):
    if "IPO" in name:
        return name.split("IPO")[0].strip() + " IPO"
    elif "SME" in name:
        return name.split("SME")[0].strip() + " SME"
    else:
        return name  # If neither, return the name as is

# Function to scrape IPO data
def scrape_ipo_data():
    url = 'https://www.investorgain.com/report/live-ipo-gmp/331/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # List to store all IPO card data
    ipo_data = []

    # Use a broader selector to target all rows with IPO data
    ipo_rows = soup.find_all('tr')[1:]  # Skip header row

    # Loop through each row of IPO data
    for row in ipo_rows:
        columns = row.find_all('td')
        if len(columns) < 11:
            continue  # Skip rows that don't have enough columns

        # Extract IPO Name and clean it (remove anything after IPO or SME)
        ipo_name = columns[0].find('a').text.strip().split(' (')[0]  # Extract name without extra text
        ipo_name = clean_ipo_name(ipo_name)  # Clean the name to ensure proper formatting

        # Extract IPO status (like "Open", "Closed", "Listing Today")
        status_span = columns[0].find('span', class_='badge')
        ipo_status = status_span.text.strip() if status_span else 'Unknown'

        # Extract complex status if available (e.g., "L@239.00 (43.98%) (Sub:156.55x)")
        complex_status_span = columns[0].find('span', class_='complex-status')
        if complex_status_span:
            complex_status = complex_status_span.text.strip()
            ipo_status += f" {complex_status}"

        # Extract Sub information from span with class "bg-secondary"
        sub_span = columns[0].find('span', class_='bg-secondary')
        ipo_sub_info = sub_span.text.strip() if sub_span else ""  # Extract Sub info like "Sub:236.8x"

        # Combine status with Sub information correctly, if Sub exists
        ipo_status_with_sub = f"{ipo_status} ({ipo_sub_info})" if ipo_sub_info else ipo_status

        # Extract Issue Price
        price = columns[1].text.strip()

        # Extract GMP from <b> tag inside <td data-label="GMP(₹)">
        gmp_td = columns[2].find('b')
        gmp = gmp_td.text.strip() if gmp_td else '0'  # Default to '0' if GMP value is not present

        # Extract Estimated Listing (Price and Percentage)
        est_listing = columns[3].text.strip()

        # Extract listing open, close, and listing date (if available)
        open_date = columns[7].text.strip()
        close_date = columns[8].text.strip()
        listing_date = columns[10].text.strip()

        # Create a dictionary for the IPO data
        ipo_info = {
            'name': ipo_name,
            'price': price,
            'gmp': gmp,
            'est_listing': est_listing,
            'open_date': open_date,
            'close_date': close_date,
            'listing_date': listing_date,
            'status': ipo_status_with_sub  # Append Sub info to status
        }

        ipo_data.append(ipo_info)

    return ipo_data

# Function to generate IPO card HTML
def generate_ipo_card_html(ipo_info):
    est_price, est_percentage = ipo_info['est_listing'].split(' ')
    est_percentage = est_percentage.strip('()%')
    
    card_html = f'''
    <div class="card" data-gmp="{ipo_info['gmp']}" data-price="{ipo_info['price']}" data-percentage="{est_percentage}" data-status="{ipo_info['status'].lower()}">
        <h2>{ipo_info['name']}</h2>
        <div class="gmp">GMP: ₹{ipo_info['gmp']}</div>
        <div class="listing-percentage">{est_percentage}%</div>
        <div class="progress-bar-container">
            <div class="progress-bar" style="width: {est_percentage}%;"></div>
        </div>
        <div class="status {ipo_info['status'][1:4].lower()}">{ipo_info['status']}</div>
        <div class="details">
            <p><span>Price:</span><span>₹{ipo_info['price']}</span></p>
            <p><span>Est Listing:</span><span>{ipo_info['est_listing']}</span></p>
            <p><span>Open:</span><span>{ipo_info['open_date']}</span></p>
            <p><span>Close:</span><span>{ipo_info['close_date']}</span></p>
            <p><span>Listing Date:</span><span>{ipo_info['listing_date']}</span></p>
        </div>
    </div>
    '''
    return card_html

# Function to check if the card already exists in the HTML
def card_exists(soup, ipo_name):
    # Assuming each card has an <h2> tag with the IPO name
    existing_cards = soup.find_all('h2')
    for card in existing_cards:
        if ipo_name in card.text:
            return True
    return False

# Function to insert the IPO cards into the existing HTML file
# Function to insert the IPO cards into the existing HTML file at the beginning
def insert_ipo_cards_into_html(ipo_data, html_file='index.html'):
    # Read the existing HTML file
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Find the cards container where new IPO cards will be added
    cards_container = soup.find(id='cards-container')

    # Track how many new cards were inserted
    inserted_cards = 0

    # Iterate over IPO data and insert only new IPO cards
    for ipo in ipo_data:
        if not card_exists(soup, ipo['name']):
            # Generate HTML for the new IPO card
            ipo_card_html = generate_ipo_card_html(ipo)
            
            # Insert the new card at the beginning of the container
            first_card = cards_container.find('div', class_='card')
            if first_card:
                first_card.insert_before(BeautifulSoup(ipo_card_html, 'html.parser'))
            else:
                # If there are no cards yet, just append
                cards_container.append(BeautifulSoup(ipo_card_html, 'html.parser'))

            inserted_cards += 1

    # Write the updated HTML content back to the file only if new cards were inserted
    if inserted_cards > 0:
        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(str(soup))

    print(f"Successfully inserted {inserted_cards} new IPO cards into {html_file}.")


# Main script execution
if __name__ == '__main__':
    ipo_data = scrape_ipo_data()
    insert_ipo_cards_into_html(ipo_data)
