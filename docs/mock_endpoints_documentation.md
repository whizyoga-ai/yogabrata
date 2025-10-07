# MCP Mock Endpoints Documentation

## Overview

This document provides comprehensive documentation for all mock MCP (Model Context Protocol) endpoints used in the Startup Formation workflow. These endpoints simulate real-world government, legal, payroll, and compliance APIs for development and testing purposes.

## Base URL

All mock endpoints are served at: `http://localhost:8001`

## Authentication

Mock endpoints simulate JWT-based authentication but do not require actual credentials for testing.

## Response Format

All endpoints return JSON responses with the following structure:

```json
{
  "field_name": "value",
  "status": "success|error",
  "timestamp": "2024-10-06T12:00:00Z",
  "processing_time": "0.1s"
}
```

## Error Simulation

Mock endpoints randomly simulate errors (5% error rate) to test error handling in the application.

## Endpoint Categories

### 1. Secretary of State Endpoints

#### 1.1 Name Availability Check
**Endpoint:** `POST /sos/name-availability`

**Purpose:** Check if a business name is available for registration.

**Request Body:**
```json
{
  "business_name": "Sample Tech LLC",
  "state": "WA",
  "entity_type": "LLC"
}
```

**Response:**
```json
{
  "available": true,
  "alternatives": [
    "TechCorp LLC",
    "Innovative Technologies LLC",
    "NextGen Solutions LLC"
  ],
  "similar_names": [],
  "processing_time": "1-2 business days"
}
```

#### 1.2 Business Entity Registration
**Endpoint:** `POST /sos/register-entity`

**Purpose:** Register a new business entity with the Secretary of State.

**Request Body:**
```json
{
  "business_name": "Sample Tech LLC",
  "entity_type": "LLC",
  "state": "WA",
  "registered_agent": {
    "name": "John Doe",
    "address": "123 Main St, Seattle, WA 98101"
  },
  "organizers": ["John Doe", "Jane Smith"],
  "management_structure": "member_managed"
}
```

**Response:**
```json
{
  "registration_number": "WA202410060001",
  "filing_date": "2024-10-06T12:00:00Z",
  "status": "filed",
  "expected_approval": "2024-10-13T12:00:00Z",
  "filing_fee": 200.00,
  "documents_required": [
    "Articles of Organization",
    "Registered Agent Information",
    "Operating Agreement"
  ]
}
```

#### 1.3 Business Search
**Endpoint:** `GET /sos/business-search`

**Purpose:** Search for existing businesses by name or registration number.

**Query Parameters:**
- `name`: Business name to search for
- `state`: State code (e.g., "WA")
- `status`: Business status filter

**Response:**
```json
{
  "businesses": [
    {
      "name": "Sample Business LLC",
      "registration_number": "WA20240001",
      "status": "active",
      "filing_date": "2024-01-15"
    }
  ],
  "total_results": 1,
  "search_criteria": "name_contains"
}
```

### 2. IRS EIN Endpoints

#### 2.1 EIN Application
**Endpoint:** `POST /irs/apply-ein`

**Purpose:** Apply for an Employer Identification Number.

**Request Body:**
```json
{
  "entity_name": "Sample Tech LLC",
  "entity_type": "LLC",
  "responsible_party": {
    "name": "John Doe",
    "ssn": "XXX-XX-1234",
    "role": "Member"
  },
  "business_address": {
    "street": "123 Main St",
    "city": "Seattle",
    "state": "WA",
    "zip": "98101"
  }
}
```

**Response:**
```json
{
  "ein": "12-3456789",
  "application_number": "E000000001",
  "status": "approved",
  "processing_time": "immediate",
  "valid_from": "2024-10-06T12:00:00Z",
  "entity_type": "LLC",
  "responsible_party": {
    "name": "John Doe",
    "ssn": "XXX-XX-1234",
    "role": "Member"
  }
}
```

#### 2.2 EIN Verification
**Endpoint:** `GET /irs/verify-ein`

**Purpose:** Verify an existing EIN and get entity information.

**Query Parameters:**
- `ein`: Employer Identification Number

**Response:**
```json
{
  "valid": true,
  "entity_name": "Sample Tech LLC",
  "ein": "12-3456789",
  "status": "active",
  "issue_date": "2024-10-06"
}
```

### 3. SAM.gov Endpoints

#### 3.1 Entity Registration
**Endpoint:** `POST /sam/register-entity`

**Purpose:** Register entity in System for Award Management.

**Request Body:**
```json
{
  "entity_name": "Sample Tech LLC",
  "ein": "12-3456789",
  "duns_number": "123456789",
  "business_types": ["LLC", "Small Business"],
  "naics_codes": ["541511"],
  "purpose_of_registration": "all_awards"
}
```

**Response:**
```json
{
  "sam_number": "SAM000001",
  "registration_status": "active",
  "expiration_date": "2025-10-06T12:00:00Z",
  "cage_code": "CAGE00001",
  "purpose_of_registration": "all_awards",
  "entity_structure": "2L",
  "business_types": ["2X", "LJ"]
}
```

### 4. Payroll System Endpoints

#### 4.1 ADP Company Setup
**Endpoint:** `POST /payroll/adp/company-setup`

**Purpose:** Set up company profile in ADP payroll system.

**Request Body:**
```json
{
  "company_name": "Sample Tech LLC",
  "ein": "12-3456789",
  "business_address": {
    "street": "123 Main St",
    "city": "Seattle",
    "state": "WA",
    "zip": "98101"
  },
  "contact_info": {
    "primary_contact": "John Doe",
    "email": "john@sampletech.com",
    "phone": "206-555-0123"
  }
}
```

**Response:**
```json
{
  "company_id": "ADP00000001",
  "setup_status": "completed",
  "monthly_cost": 45.00,
  "features_enabled": [
    "payroll_processing",
    "tax_filing",
    "direct_deposit",
    "employee_portal"
  ],
  "estimated_setup_time": "2-3 business days"
}
```

#### 4.2 Gusto Company Setup
**Endpoint:** `POST /payroll/gusto/company-setup`

**Purpose:** Set up company profile in Gusto payroll system.

**Request Body:** (Same as ADP)

**Response:**
```json
{
  "company_uuid": "gusto_1234567890abcdef",
  "setup_status": "completed",
  "monthly_cost": 40.00,
  "features_enabled": [
    "payroll_processing",
    "benefits_administration",
    "time_tracking",
    "contractor_payments"
  ],
  "onboarding_steps": [
    "Complete company profile",
    "Add employees",
    "Configure payroll schedule",
    "Setup tax information"
  ]
}
```

#### 4.3 Paychex Company Setup
**Endpoint:** `POST /payroll/paychex/company-setup`

**Purpose:** Set up company profile in Paychex payroll system.

**Request Body:** (Same as ADP)

**Response:**
```json
{
  "company_code": "PC000001",
  "setup_status": "completed",
  "monthly_cost": 50.00,
  "features_enabled": [
    "payroll_processing",
    "hr_services",
    "time_and_attendance",
    "retirement_services"
  ],
  "implementation_timeline": "5-7 business days"
}
```

### 5. Legal Compliance Endpoints

#### 5.1 US Code Search
**Endpoint:** `GET /legal/us-code/search`

**Purpose:** Search US Code for relevant legal requirements.

**Query Parameters:**
- `title`: US Code title (e.g., "26")
- `section`: Specific section
- `keywords`: Search keywords

**Response:**
```json
{
  "title": "26 U.S. Code Chapter 1 - Normal Taxes and Surtaxes",
  "sections": [
    {
      "section": "§ 6012. Persons required to make returns of income",
      "content": "Returns with respect to income taxes under subtitle A shall be made by the following...",
      "last_updated": "2024-01-01"
    }
  ],
  "total_sections": 1,
  "search_terms": "business_tax_obligation"
}
```

#### 5.2 CFR Search
**Endpoint:** `GET /legal/cfr/search`

**Purpose:** Search Code of Federal Regulations.

**Query Parameters:** (Same as US Code)

**Response:**
```json
{
  "title": "26 CFR Part 1 - Income Tax Regulations",
  "parts": [
    {
      "part": "§ 1.6012-2. Corporations required to make returns of income",
      "content": "Every corporation, as defined in section 7701(a)(3), shall make a return of income...",
      "effective_date": "2024-01-01"
    }
  ],
  "total_parts": 1,
  "search_terms": "corporate_tax_filing"
}
```

#### 5.3 State Statutes Search
**Endpoint:** `GET /legal/state-statutes/search`

**Purpose:** Search state-specific statutes and regulations.

**Query Parameters:**
- `state`: State code (e.g., "WA")
- `title`: Statute title
- `keywords`: Search keywords

**Response:**
```json
{
  "state": "Washington",
  "title": "Revised Code of Washington (RCW)",
  "chapters": [
    {
      "chapter": "23B.01.200 - Filing requirements",
      "content": "The articles of incorporation must be filed with the secretary of state...",
      "last_updated": "2024-01-01"
    }
  ],
  "total_chapters": 1,
  "search_terms": "business_registration"
}
```

### 6. State Tax Authority Endpoints

#### 6.1 Washington DOR Registration
**Endpoint:** `POST /tax/wa-dor/register`

**Purpose:** Register for Washington State taxes.

**Request Body:**
```json
{
  "business_name": "Sample Tech LLC",
  "ein": "12-3456789",
  "business_address": {
    "street": "123 Main St",
    "city": "Seattle",
    "state": "WA",
    "zip": "98101"
  },
  "tax_types": ["business_occupation", "sales_tax"],
  "filing_frequency": "quarterly"
}
```

**Response:**
```json
{
  "tax_registration_number": "WA000000001",
  "accounts_created": [
    "Business & Occupation Tax",
    "Sales Tax",
    "Use Tax"
  ],
  "filing_frequency": "quarterly",
  "first_filing_due": "2025-01-31T23:59:59Z",
  "quarterly_due_dates": [
    "January 31",
    "April 30",
    "July 31",
    "October 31"
  ]
}
```

#### 6.2 Tax Status Check
**Endpoint:** `GET /tax/wa-dor/status`

**Purpose:** Check tax account status and compliance.

**Query Parameters:**
- `registration_number`: Tax registration number

**Response:**
```json
{
  "status": "active",
  "accounts": [
    {
      "type": "Business & Occupation Tax",
      "account_number": "B00000001",
      "status": "active",
      "last_filing": "2024-07-31"
    }
  ],
  "compliance_status": "good_standing",
  "next_filing_due": "2024-10-31"
}
```

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "error": "Error description",
  "code": "ERROR_CODE",
  "details": "Additional error details",
  "timestamp": "2024-10-06T12:00:00Z"
}
```

Common error codes:
- `VALIDATION_ERROR`: Invalid request data
- `NOT_FOUND`: Resource not found
- `RATE_LIMITED`: Too many requests
- `SERVER_ERROR`: Internal server error

## Rate Limiting

Mock endpoints simulate rate limiting:
- Default: 10 requests per minute per endpoint
- Some endpoints have lower limits (e.g., government APIs: 5/min)

## Testing the Endpoints

### Using curl:

```bash
# Check name availability
curl -X POST http://localhost:8001/sos/name-availability \
  -H "Content-Type: application/json" \
  -d '{"business_name": "Sample Tech LLC", "state": "WA"}'

# Apply for EIN
curl -X POST http://localhost:8001/irs/apply-ein \
  -H "Content-Type: application/json" \
  -d '{"entity_name": "Sample Tech LLC", "entity_type": "LLC"}'

# Search businesses
curl "http://localhost:8001/sos/business-search?name=Sample"
```

### Using the Mock Admin API:

```bash
# Get endpoint statistics
curl http://localhost:8001/mock-admin/stats

# Clear request history
curl -X POST http://localhost:8001/mock-admin/clear-history
```

## Integration Notes

1. **Environment Toggle**: Use environment variables to switch between mock and live endpoints:
   ```bash
   export USE_MOCK_SERVERS=true
   ```

2. **Error Handling**: All endpoints simulate realistic error conditions for testing error handling.

3. **Data Consistency**: Mock responses use consistent data patterns for testing workflows.

4. **Performance**: Endpoints simulate realistic response times (100ms - 2s).

## Future Integration

When integrating with real APIs:

1. Replace mock base URLs with actual API endpoints
2. Implement proper authentication mechanisms
3. Add retry logic for failed requests
4. Implement proper rate limiting
5. Add comprehensive logging and monitoring

## Support

For questions about mock endpoints or integration issues, refer to:
- Mock server logs: Check `/mock-admin/stats` endpoint
- Request history: Available via admin endpoints
- Error patterns: Documented in this specification
