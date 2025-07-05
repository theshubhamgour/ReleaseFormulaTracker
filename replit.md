# Release Configuration Tracker

## Overview

The Release Configuration Tracker is a Streamlit-based web application designed to process Excel workbooks containing product configuration formulas and generate release image stacks. The application extracts formulas from Excel files, analyzes them, and maps them to microservice components for deployment planning.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application
- **Configuration**: Single-page application with file upload capabilities
- **UI Components**: File uploader, data display tables, processing status indicators
- **Session Management**: Streamlit session state for maintaining application state across interactions

### Backend Architecture
- **Language**: Python 3.11
- **Architecture Pattern**: Modular service-oriented design
- **Core Components**:
  - Formula processing engine
  - Stack generation service
  - Excel file parser

### Processing Pipeline
1. **File Upload**: Excel workbook (.xlsx) upload via Streamlit interface
2. **Formula Extraction**: Parse Excel formulas using openpyxl library
3. **Formula Analysis**: Categorize and analyze extracted formulas
4. **Stack Generation**: Map formulas to microservice components and generate deployment stacks

## Key Components

### FormulaProcessor (`formula_processor.py`)
- **Purpose**: Extracts and analyzes Excel formulas from workbooks
- **Key Features**:
  - Pattern matching for 20+ Excel function types (VLOOKUP, IF, SUM, etc.)
  - Formula categorization and metadata extraction
  - Error handling for malformed formulas
- **Design Decision**: Uses regex patterns for formula detection to handle various Excel function formats

### StackGenerator (`stack_generator.py`)
- **Purpose**: Converts Excel formulas into microservice stack definitions
- **Key Features**:
  - Maps Excel functions to service types (data-service, logic-service, calculation-service, etc.)
  - Defines service dependencies and categories
  - Generates deployment-ready stack configurations
- **Design Decision**: Uses a mapping-based approach to translate Excel functionality to cloud services

### Main Application (`app.py`)
- **Purpose**: Streamlit web interface and application orchestration
- **Key Features**:
  - File upload handling
  - Session state management
  - Progress indicators and error handling
  - Results display and visualization

## Data Flow

1. **Upload Phase**: User uploads Excel workbook through Streamlit interface
2. **Processing Phase**: 
   - FormulaProcessor extracts formulas from all worksheets
   - Formulas are categorized and analyzed for complexity
3. **Generation Phase**:
   - StackGenerator maps formulas to service components
   - Service dependencies are resolved
   - Release stack configuration is generated
4. **Display Phase**: Results are presented in the web interface

## External Dependencies

### Core Libraries
- **streamlit**: Web application framework for the user interface
- **openpyxl**: Excel file parsing and formula extraction
- **pandas**: Data manipulation and analysis (planned usage)

### Runtime Environment
- **Python**: 3.11 runtime environment
- **Nix**: Package management via stable-24_05 channel
- **Replit**: Cloud deployment platform with autoscale configuration

### Service Mappings
The application maps Excel functions to the following service categories:
- Data services (lookup, filtering, deduplication)
- Logic services (conditional, selection)
- Calculation services (math, aggregation)
- Text services (formatting)
- Date services (temporal operations)
- Reference services (dynamic references)

## Deployment Strategy

### Platform
- **Environment**: Replit cloud platform
- **Scaling**: Autoscale deployment target
- **Runtime**: Python 3.11 with Nix package management

### Configuration
- **Port**: 5000 (configured in both .replit and Streamlit config)
- **Server**: Headless mode with public address binding
- **Workflow**: Parallel execution with shell command integration

### Startup Process
1. Nix environment initialization with required packages
2. Streamlit server startup on port 5000
3. Application module loading and initialization

## Changelog

```
Changelog:
- June 27, 2025. Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```

## Technical Notes

### Architecture Decisions
- **Streamlit Choice**: Selected for rapid prototyping and easy deployment without frontend complexity
- **openpyxl Library**: Chosen over pandas.read_excel() to access formula strings (not just calculated values)
- **Modular Design**: Separated concerns into distinct processor classes for maintainability
- **Session State**: Used Streamlit session state instead of external storage for simplicity

### Limitations and Considerations
- Currently processes .xlsx files only (no .xls support)
- Formula extraction may not handle all Excel function variations
- Stack generation mappings are predefined and may need customization
- No persistent storage - all data is session-based

### Extension Points
- Database integration could be added for formula storage and analysis
- Additional Excel function support can be extended via pattern matching
- Custom service mapping configurations could be made user-configurable
- Export functionality for generated stack configurations