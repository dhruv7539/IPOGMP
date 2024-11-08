
# IPO GMP Tracker

**An IPO GMP Tracker application that provides a comprehensive list of IPOs with essential details such as open and close dates, GMP percentages, and more. This tool is designed to help users quickly access and filter IPO information for better investment insights.**

## Features

- **IPO List with Key Details**: 
  - **Open Date**
  - **Close Date**
  - **GMP (Grey Market Premium) Percentage**
  - Additional IPO-related information for informed decision-making.
  
- **Powerful Filtering Options**:
  - Sort IPOs by **GMP Percentage**: Easily rank IPOs based on their GMP, giving insights into current demand.
  - Sort by **Recent Listings**: View the latest IPOs at a glance.
  
- **User-Friendly Interface**:
  - Clean, intuitive design for seamless navigation.
  - Quick filters for efficient information retrieval.

## Getting Started

To set up the IPO GMP Tracker locally, follow these steps:

### Clone the Repository
```bash
git clone https://github.com/yourusername/ipo-gmp-tracker.git
```

### Install Dependencies
```bash
cd ipo-gmp-tracker
npm install
```

### Configure Environment Variables
Create a `.env` file in the project root and add necessary environment variables. For example:

```plaintext
DB_URI=your_database_uri
API_KEY=your_api_key
```

### Run the Application
```bash
npm start
```

### Open in Browser
Access the application at `http://localhost:3000`.

## Usage

1. Launch the app to see the IPO listings.
2. Use filters to:
   - Sort IPOs by **GMP Percentage**.
   - List the most **recent IPOs** at the top.
3. Click on an IPO entry for detailed insights.

## Technologies Used

- **Frontend**: React
- **Backend**: Node.js, Express
- **Database**: MongoDB (or your choice)
- **Others**: Chart.js for GMP visualization, if applicable

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License.
