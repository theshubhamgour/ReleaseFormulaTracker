# Release Configuration Tracker

A Streamlit-based web application that processes Excel workbooks to extract formulas and generate release image stacks for microservice deployments.

## Features

- **Excel Processing**: Upload and process Excel workbooks with progress tracking
- **Release Version Selection**: Extract and select from pre-release versions 
- **Stack Generation**: Generate Docker image stacks based on Excel formulas
- **Interactive UI**: Clean web interface with progress indicators and data tables

## Requirements

- Python 3.11 or higher
- pip (Python package manager)

## Installation

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd release-configuration-tracker
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install the packages manually:

```bash
pip install streamlit openpyxl pandas
```

## Running the Application

### Start the Streamlit Server

```bash
streamlit run app.py
```

The application will start and display:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Access the Application

Open your web browser and navigate to:
- **Local**: http://localhost:8501
- **Network**: Use the network URL if accessing from other devices

## Usage

### Step 1: Upload Excel File
1. Click "Choose an Excel file" button
2. Select your `.xlsx` file
3. Watch the progress bar (0-100%) as the file processes

### Step 2: Select Release Version
1. After processing, use the dropdown to select a release version
2. Versions are extracted from the 'product-pre-release-neewee' sheet starting at B6

### Step 3: Generate Stack
1. Click "Generate Stack" button
2. The application will:
   - Update B5 cell in 'pre-release-version' sheet with selected version
   - Process Excel formulas to extract service data
   - Display results in a table format

### Expected Output
The generated stack will show:
- **Service Name**: Extracted from Excel formulas
- **Docker Image**: Generated image names in format `neewee/servicename:pre-release-vX.X.X`

## Project Structure

```
release-configuration-tracker/
├── app.py                 # Main Streamlit application
├── formula_processor.py   # Excel formula processing logic
├── stack_generator.py     # Stack generation and Docker image creation
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── replit.md             # Project documentation and architecture
```

## Configuration

The application expects your Excel workbook to have:
- **'product-pre-release-neewee'** sheet with release versions starting at B6
- **'pre-release-version'** sheet with B5 cell for version input
- Service names and formulas in the target sheets

## Troubleshooting

### Common Issues

1. **Module not found errors**
   ```bash
   pip install streamlit openpyxl pandas
   ```

2. **Excel file not processing**
   - Ensure file is in `.xlsx` format
   - Check that required sheets exist in the workbook
   - Verify sheet names match exactly: 'product-pre-release-neewee', 'pre-release-version'

3. **No release versions found**
   - Check that 'product-pre-release-neewee' sheet exists
   - Verify data starts at cell B6
   - Ensure cells contain actual values (not empty)

4. **Port already in use**
   ```bash
   streamlit run app.py --server.port 8502
   ```

### Debug Mode

To see detailed processing information, the application shows:
- Available sheet names
- Number of release versions found
- Processing status messages

## Development

### Adding New Features

1. **Formula Processing**: Modify `formula_processor.py`
2. **Stack Generation**: Update `stack_generator.py` 
3. **UI Changes**: Edit `app.py`

### Running in Development Mode

```bash
# Enable debug mode
streamlit run app.py --server.runOnSave true
```

## Dependencies

- **streamlit**: Web application framework
- **openpyxl**: Excel file processing
- **pandas**: Data manipulation (optional)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your Excel file structure matches requirements
3. Ensure all dependencies are installed correctly

## License

This project is for internal use. Please refer to your organization's licensing terms.