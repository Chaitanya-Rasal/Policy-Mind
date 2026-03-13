
# UML Diagrams for Legal/Policy Document Summarizer & Q&A System

This directory contains comprehensive PlantUML diagrams documenting the system architecture, workflows, and data structures.

## Diagram Index

### 1. **Use Case Diagram** (`01_use_case_diagram.puml`)
Shows user interactions with the system, including upload, summarization, and Q&A features.

### 2. **Class Diagram** (`02_class_diagram.puml`)
Depicts the object-oriented structure of the backend modules, routes, and their relationships.

### 3. **Sequence Diagram - Upload** (`03_sequence_upload.puml`)
Detailed flow of document upload, text extraction, chunking, and FAISS index creation.

### 4. **Sequence Diagram - Summarize** (`04_sequence_summarize.puml`)
Shows the summary generation process using Gemini 2.5 Flash.

### 5. **Sequence Diagram - Q&A** (`05_sequence_qa.puml`)
Illustrates the RAG (Retrieval-Augmented Generation) workflow for question answering.

### 6. **Activity Diagram** (`06_activity_diagram.puml`)
Complete user workflow from upload through summarization and Q&A.

### 7. **Component Diagram** (`07_component_diagram.puml`)
System architecture showing frontend, backend layers, and external services.

### 8. **Deployment Diagram** (`08_deployment_diagram.puml`)
Runtime architecture on Replit with file system and Google AI services.

### 9. **State Diagram** (`09_state_diagram.puml`)
Document processing states from upload through ready state with concurrent Q&A.

### 10. **Package Diagram** (`10_package_diagram.puml`)
Module organization and dependencies.

### 11. **ERD Diagram** (`11_erd_diagram.puml`)
Data structures, entities, and their relationships (runtime and persistent).

## Rendering the Diagrams

### Online Rendering

1. **PlantUML Online Editor**: https://www.plantuml.com/plantuml/uml/
   - Copy and paste the `.puml` file contents
   - View/download as PNG, SVG, or PDF

2. **PlantText**: https://www.planttext.com/
   - Paste code and render instantly

### Local Rendering

#### Prerequisites
```bash
# Install PlantUML
brew install plantuml  # macOS
# or
apt-get install plantuml  # Ubuntu/Debian
```

#### Generate PNG Images
```bash
# Generate all diagrams
plantuml docs/uml/*.puml

# Generate specific diagram
plantuml docs/uml/01_use_case_diagram.puml

# Generate as SVG (scalable)
plantuml -tsvg docs/uml/*.puml
```

#### Generate PDF
```bash
plantuml -tpdf docs/uml/*.puml
```

### VS Code Extension

Install **PlantUML** extension:
1. Open VS Code
2. Install extension: `jebbs.plantuml`
3. Right-click on `.puml` file → "Preview Current Diagram"
4. Export as PNG/SVG from preview

## Diagram Conventions

### Color Coding
- **Light Blue**: Processing/computation steps
- **Light Green**: Data storage operations
- **Light Yellow**: Decision points
- **Light Red**: Error states

### Annotations
- **Notes**: Provide additional context and explanations
- **Stereotypes**: Indicate patterns (<<include>>, <<extend>>, etc.)
- **Multiplicities**: Show cardinality in relationships

### Naming Conventions
- **Classes/Components**: PascalCase
- **Methods/Functions**: snake_case
- **Variables**: snake_case
- **Constants**: UPPER_SNAKE_CASE

## Key Insights from Diagrams

### Architecture Patterns
1. **Modular Design**: Clear separation between routes, modules, and utils
2. **Singleton Pattern**: AIService and Config classes
3. **Repository Pattern**: EmbeddingService manages FAISS persistence
4. **RAG Architecture**: Retrieval-Augmented Generation for Q&A

### Performance Bottlenecks
1. **Embedding Generation**: 1-2 seconds per chunk (identified in sequence diagrams)
2. **API Rate Limits**: 2 requests/minute for free tier (noted in deployment)
3. **Text Extraction**: Variable time based on document size

### Error Handling
- Comprehensive error states in state diagram
- Validation at multiple layers (frontend, routes, modules)
- Graceful degradation for API quota issues

### Data Flow
1. Upload → Extract → Chunk → Embed → Index (one-way)
2. Question → Embed → Search → Retrieve → Answer (bidirectional with FAISS)
3. Summary: Document → Truncate → Generate (stateless)

## Maintenance

When updating the system:
1. Update relevant `.puml` files
2. Regenerate images
3. Update this README if adding new diagrams
4. Commit both `.puml` files and generated images (if stored)

## References

- PlantUML Documentation: https://plantuml.com/
- PlantUML Language Reference: https://plantuml.com/guide
- UML Best Practices: https://www.visual-paradigm.com/guide/uml/

## Questions?

Refer to:
- `PROJECT.md` - Overall project documentation
- `MODULES.md` - Detailed module documentation
- Source code comments for implementation details
