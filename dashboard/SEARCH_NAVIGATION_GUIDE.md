# Search and Navigation Feature Guide

## Overview

The Search and Navigation feature provides comprehensive filtering, sorting, and pagination capabilities for uploaded loan documents in the dashboard. This feature addresses Requirements 7.2 and 7.3 from the specification.

## Features Implemented

### 1. Search Functionality
- **Text Search**: Search documents by filename
- **Real-time Filtering**: Results update as you type
- **Case-insensitive**: Searches work regardless of letter case

### 2. Filter Options

#### Loan Type Filter
- Filter documents by loan type (Education, Home, Personal, Vehicle, Gold)
- Dropdown selection with "All" option
- Automatically extracts unique loan types from uploaded documents

#### Bank Name Filter
- Filter documents by lending institution
- Dropdown selection with "All" option
- Automatically extracts unique bank names from uploaded documents

#### Date Range Filter
- **Predefined Ranges**:
  - All Time (default)
  - Today
  - Last 7 Days
  - Last 30 Days
  - Custom Range
- **Custom Range**: Select specific start and end dates
- Filters based on document upload date

### 3. Sorting Options

Documents can be sorted by:
- **Upload Date**: Newest first or Oldest first
- **Name**: Alphabetical (A-Z or Z-A)
- **Principal Amount**: High to Low or Low to High
- **Interest Rate**: High to Low or Low to High

### 4. Pagination

- **Configurable Page Size**: 5, 10, 20, or 50 items per page
- **Navigation Controls**:
  - First Page button
  - Previous Page button
  - Next Page button
  - Last Page button
  - Direct page jump with number input
- **Page Information**: Shows current page, total pages, and item range

### 5. View Modes

#### Grid View
- Displays 2 documents per row
- Card-based layout with key information
- Quick action buttons (View, Compare, Download)
- Visual and easy to scan

#### List View
- Tabular layout with all documents
- Compact display showing:
  - Document name
  - Loan type
  - Bank name
  - Principal amount
  - Interest rate
  - Action button
- Efficient for reviewing many documents

### 6. Search Summary

Displays aggregate statistics for filtered results:
- Total number of documents
- Average principal amount
- Average interest rate
- Number of unique banks

## Usage

### Accessing the Search Feature

1. Navigate to the dashboard
2. Click on the "🔍 Search & Filter" tab
3. The search interface will load with all uploaded documents

### Basic Search

1. Enter text in the "Search by document name" field
2. Results filter automatically as you type
3. Clear the search box to see all documents again

### Applying Filters

1. **Loan Type**: Select from dropdown (e.g., "Education Loan")
2. **Bank Name**: Select from dropdown (e.g., "ABC Bank")
3. **Date Range**: Choose a predefined range or select custom dates
4. Filters can be combined for more specific results
5. Click "Clear All Filters" to reset

### Sorting Results

1. Select sorting criteria from the "Sort by" dropdown
2. Results update immediately
3. Sorting works with filtered results

### Changing View Mode

1. Select "Grid" or "List" from the View dropdown
2. Layout changes immediately
3. Preference is maintained while browsing

### Pagination

1. Use navigation buttons to move between pages
2. Change "Items per page" to adjust page size
3. Use "Jump to page" for direct navigation
4. Page information shows your current position

### Viewing Documents

1. Click "View" button on any document card/row
2. Redirects to detailed document view
3. Can return to search results to view another document

## Technical Implementation

### Component Structure

```
dashboard/components/search.py
├── render_search_interface()      # Main entry point
├── get_unique_loan_types()        # Extract unique loan types
├── get_unique_bank_names()        # Extract unique bank names
├── filter_documents()             # Apply all filters
├── sort_documents()               # Sort by criteria
├── display_grid_view()            # Render grid layout
├── display_list_view()            # Render list layout
├── render_document_card()         # Individual card in grid
├── render_document_list_item()    # Individual row in list
├── render_pagination_controls()   # Pagination UI
└── render_search_summary()        # Statistics display
```

### Session State Variables

- `search_page`: Current page number (default: 1)
- `search_page_size`: Items per page (default: 10)
- `uploaded_documents`: List of all uploaded documents
- `selected_document`: Currently selected document for viewing
- `current_view`: Current tab/view in the dashboard

### Data Requirements

Each document in `uploaded_documents` should have:
```python
{
    "name": str,              # Document filename
    "size": int,              # File size in bytes
    "type": str,              # MIME type
    "content": bytes,         # File content
    "upload_date": date,      # Upload date (added automatically)
    "extracted_data": {       # Extracted loan information
        "loan_type": str,
        "bank_name": str,
        "principal_amount": float,
        "interest_rate": float,
        "tenure_months": int,
        ...
    }
}
```

## Integration

### Dashboard Integration

The search component is integrated into the main dashboard (`app.py`):

```python
# Import at top of file
from search import render_search_interface

# Add tab in main()
tab1, tab2, tab3, tab4 = st.tabs([
    "📤 Upload & Extract", 
    "🔍 Search & Filter",  # New tab
    "📊 View Results", 
    "ℹ️ About"
])

# Render in tab
with tab2:
    show_search_tab()

# Function definition
def show_search_tab():
    """Search and filter tab"""
    try:
        from search import render_search_interface
        render_search_interface()
    except ImportError as e:
        st.error(f"Error loading search component: {e}")
```

### Upload Component Integration

The upload component (`upload.py`) was updated to add upload dates:

```python
from datetime import datetime

# When adding document to session state
st.session_state.uploaded_documents.append({
    # ... other fields ...
    "upload_date": datetime.now().date()  # Add upload date
})
```

## Testing

### Manual Testing Checklist

- [ ] Search by document name works
- [ ] Loan type filter works
- [ ] Bank name filter works
- [ ] Date filters work (Today, Last 7 Days, Last 30 Days)
- [ ] Custom date range works
- [ ] Combined filters work together
- [ ] Sorting by name works (A-Z and Z-A)
- [ ] Sorting by principal amount works
- [ ] Sorting by interest rate works
- [ ] Sorting by upload date works
- [ ] Grid view displays correctly
- [ ] List view displays correctly
- [ ] Pagination navigation works
- [ ] Page size change works
- [ ] Direct page jump works
- [ ] View button redirects correctly
- [ ] Download button works
- [ ] Clear filters button resets all filters
- [ ] Search summary displays correct statistics

### Automated Tests

Run the test suite:
```bash
python Lab3/tests/test_search_functionality.py
```

Tests cover:
- Extracting unique loan types and bank names
- Filtering by search query
- Filtering by loan type
- Filtering by bank name
- Filtering by date range
- Sorting by name
- Sorting by principal amount
- Sorting by interest rate
- Combined filters

## Performance Considerations

### Optimization Strategies

1. **Client-side Filtering**: All filtering and sorting happens in memory
2. **Lazy Loading**: Only current page documents are rendered
3. **Session State**: Maintains state across interactions
4. **Efficient Sorting**: Uses Python's built-in sorted() with key functions

### Scalability

- Current implementation handles up to ~1000 documents efficiently
- For larger datasets, consider:
  - Backend API integration for filtering/sorting
  - Database queries instead of in-memory filtering
  - Virtual scrolling instead of pagination
  - Caching of filter results

## Future Enhancements

### Potential Improvements

1. **Advanced Search**:
   - Search by principal amount range
   - Search by interest rate range
   - Search by tenure
   - Full-text search in extracted data

2. **Saved Searches**:
   - Save filter combinations
   - Quick access to common searches
   - Share search URLs

3. **Bulk Actions**:
   - Select multiple documents
   - Bulk download
   - Bulk comparison
   - Bulk delete

4. **Export Options**:
   - Export search results to CSV
   - Export to Excel
   - Generate PDF report

5. **Advanced Sorting**:
   - Multi-column sorting
   - Custom sort order
   - Save sort preferences

6. **Visualization**:
   - Charts showing distribution by loan type
   - Timeline view of uploads
   - Comparison charts

## Troubleshooting

### Common Issues

**Issue**: Search returns no results
- **Solution**: Check if documents are uploaded and have extracted data
- **Solution**: Verify filter criteria aren't too restrictive

**Issue**: Pagination not working
- **Solution**: Check if `search_page` is in session state
- **Solution**: Verify total_pages calculation is correct

**Issue**: Sorting not working
- **Solution**: Ensure extracted_data contains the field being sorted
- **Solution**: Check for None values in sort fields

**Issue**: Date filter not working
- **Solution**: Verify documents have `upload_date` field
- **Solution**: Check date format is `datetime.date` object

## Requirements Mapping

This implementation satisfies the following requirements:

### Requirement 7.2
> THE Platform SHALL provide navigation controls within the Dashboard

**Implementation**:
- Pagination controls (First, Previous, Next, Last)
- Page jump functionality
- View mode switching (Grid/List)
- Tab navigation integration

### Requirement 7.3
> THE Platform SHALL provide search functionality for uploaded documents

**Implementation**:
- Text search by document name
- Filter by loan type
- Filter by bank name
- Filter by date range
- Combined filtering support
- Real-time search results

## Conclusion

The Search and Navigation feature provides a comprehensive solution for managing and finding loan documents in the dashboard. It offers multiple ways to filter, sort, and view documents, making it easy for users to find the information they need quickly and efficiently.
