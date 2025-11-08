# Search and Navigation Feature

## Overview

The search and navigation feature allows users to quickly find and filter uploaded loan documents based on various criteria. This feature implements requirements 7.2 and 7.3 from the design specification.

## Features

### 1. Search Filters

#### Basic Filters
- **Document Name**: Search by filename or partial filename match
- **Loan Type**: Filter by loan category (Education, Home, Personal, Vehicle, Gold, Other)
- **Bank Name**: Filter by lending institution name

#### Advanced Filters
- **Upload Date Range**: Filter documents uploaded within a specific date range
- **Principal Amount Range**: Filter by minimum and maximum loan amounts
- **Interest Rate Range**: Filter by interest rate percentage

### 2. Search Results

The search results display:
- Total number of matching documents
- Sortable results by:
  - Upload Date
  - Principal Amount
  - Interest Rate
  - Bank Name
  - Loan Type
- Ascending or descending sort order

### 3. Loan Cards

Each loan document is displayed in a card format showing:
- Bank name and loan type
- Principal amount and currency
- Interest rate and tenure
- Quick "View" button to see full details
- Expandable section with:
  - Moratorium period
  - Repayment mode
  - Fee details
  - Extraction confidence score
  - Co-signer information (if applicable)

### 4. Pagination

For large result sets:
- Results are paginated (10 items per page)
- Navigation controls:
  - First page
  - Previous page
  - Next page
  - Last page
- Page number input for direct navigation

### 5. Navigation Controls

#### Breadcrumb Navigation
- Shows current location in the application
- Format: 🏠 Home > [Current View]

#### Quick Actions Sidebar
- Upload New Document
- Search Documents
- Compare Loans
- Quick access from any page

## Usage

### Basic Search

1. Navigate to "Search Documents" from the sidebar
2. Enter search criteria in the filter fields
3. Click "🔍 Search" button
4. Browse results and click "View" to see full details

### Advanced Search

1. Click "Advanced Filters" to expand additional options
2. Set date ranges, amount ranges, or interest rate ranges
3. Click "🔍 Search" to apply all filters
4. Use "Clear Filters" to reset all search criteria

### Sorting Results

1. Use the "Sort by" dropdown to select sorting field
2. Choose "Ascending" or "Descending" order
3. Results update automatically

### Navigating Results

1. Use pagination controls at the bottom of results
2. Enter a specific page number to jump directly
3. Click loan cards to expand details
4. Click "View" button to navigate to full document view

## API Integration

The search feature communicates with the backend API using the following endpoint:

```python
GET /api/v1/loans?[filters]
```

### Query Parameters

- `file_name`: Document filename filter
- `loan_type`: Loan type filter (education, home, personal, vehicle, gold, other)
- `bank_name`: Bank name filter
- `upload_date_from`: Start date for upload range (ISO format)
- `upload_date_to`: End date for upload range (ISO format)
- `principal_min`: Minimum principal amount
- `principal_max`: Maximum principal amount
- `interest_rate_min`: Minimum interest rate
- `interest_rate_max`: Maximum interest rate

## Technical Implementation

### Components

- **`search.py`**: Main search interface component
  - `render_search_interface()`: Main search UI
  - `render_loan_card()`: Individual loan card display
  - `render_pagination_controls()`: Pagination navigation
  - `render_quick_navigation()`: Sidebar quick actions
  - `render_breadcrumb_navigation()`: Breadcrumb display

### Session State

The feature uses Streamlit session state to maintain:
- `current_view`: Current page/view
- `selected_document`: Currently selected document ID
- `search_page`: Current pagination page

### Error Handling

- API connection errors display user-friendly messages
- Missing data fields show "N/A" placeholders
- Sorting failures fall back to original order
- Empty results show informative message

## Future Enhancements

Potential improvements for future versions:
- Saved search filters
- Export search results to CSV/Excel
- Bulk actions on search results
- Search history
- Advanced query builder
- Full-text search across document content
- Fuzzy matching for bank names
- Auto-complete for search fields
