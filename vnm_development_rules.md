# VNM DEVELOPMENT RULES AND PRIMITIVES

## CORE PRIMITIVES

### Simple Solutions Axiom
- Always choose the simplest solution that achieves the objective
- Avoid over-engineering and unnecessary complexity
- Prefer straightforward, maintainable approaches
- "If it can be simpler, make it simpler"

### Explicit Documentation Requirement
- Every decision, change, and configuration must be documented
- Code comments explain "why", not just "what"
- Architecture decisions recorded and justified
- Documentation updated with every significant change

### Incremental Development Approach
- Break complex tasks into smaller, manageable phases
- Test and validate each phase before proceeding
- Iterative improvement over big-bang changes
- Continuous feedback and adjustment

## DEVELOPMENT ENVIRONMENT
- User development environment: Windows with Docker container only for data base and manage data base
- Frontend and backend without containers
- Database runs in PostgreSQL container with PostGIS
- All development tooling runs locally for optimal performance and debugging

## DEVELOPMENT WORKFLOW
- Frontend and backend without containers
- Database runs in PostgreSQL container with PostGIS
- Local debugging configurations in VS Code
- Hot reload enabled for both frontend and backend
- Direct console.log visibility and breakpoint functionality

## CODE QUALITY STANDARDS
- TypeScript for frontend components where applicable
- Python type hints for backend functions
- Comprehensive error handling and logging
- Unit tests for critical business logic
- Integration tests for API endpoints

## DEBUGGING REQUIREMENTS
- VS Code debugging configurations must work reliably
- Source maps enabled for frontend debugging
- Python debugging with breakpoints for backend
- Full-stack debugging capability
- Console logs must be visible and functional

## SECURITY GUIDELINES
- Environment variables for sensitive configuration
- JWT tokens for authentication
- CORS properly configured
- SQL injection prevention with parameterized queries
- Input validation on all endpoints

## DATABASE STANDARDS
- PostgreSQL with PostGIS for spatial data
- Proper indexing for performance
- Migration scripts for schema changes
- Backup procedures documented
- Development data seeding automated

---

*Last updated: 2025-10-19 - Post Docker simplification*