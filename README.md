# Simplified Codebase-to-Course Generator

A simplified version of the codebase-to-course skill that analyzes Python codebases and generates interactive HTML courses. This tool helps you understand any Python project by creating beautiful, interactive documentation.

## What is this?

This is a simplified version of the original [Codebase-to-Course](https://github.com/user/codebase-to-course) skill. It takes a Python codebase and generates an interactive HTML course that teaches how the code works through:

- **Scroll-based modules** with progress tracking
- **Code ↔ Plain English translations** - real code alongside explanations
- **Interactive quizzes** that test understanding
- **Visual architecture diagrams** and component overviews
- **Glossary tooltips** for technical terms

## Who is this for?

This tool is designed for **"vibe coders"** — people who build software by instructing AI coding tools in natural language, without a traditional CS education.

**Your goals are practical, not academic:**
- Steer AI coding tools better (make smarter architectural decisions)
- Detect when AI is wrong (spot hallucinations, catch bad patterns)
- Debug when AI gets stuck (break out of bug loops)
- Talk to engineers without feeling lost

## Features

### 🔍 Codebase Analysis
- Automatically analyzes Python files using AST parsing
- Extracts classes, functions, imports, and module structure
- Identifies main entry points and application architecture
- Calculates complexity scores

### 📚 Interactive Course Generation
- Creates 5 comprehensive modules covering:
  1. **Introduction** - What the project does
  2. **Architecture** - How it's structured
  3. **Components** - Key classes and their responsibilities
  4. **Data Flow** - How data moves through the system
  5. **Interactive Elements** - Key functions and usage patterns

### 🎨 Beautiful Design
- Warm, inviting design inspired by developer notebooks
- Responsive layout that works on desktop and mobile
- Smooth animations and scroll interactions
- Custom typography with Bricolage Grotesque, DM Sans, and JetBrains Mono

### 🧩 Interactive Elements
- Code ↔ Plain English translation blocks
- Multiple-choice quizzes with instant feedback
- Visual component cards and architecture diagrams
- Callout boxes for key insights

## Installation

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Setup
1. Clone or download this repository
2. Navigate to the project directory
3. Run the generator:

```bash
# Basic usage
python main.py /path/to/your/codebase

# With custom output directory
python main.py /path/to/your/codebase ./my-course

# With verbose output
python main.py /path/to/your/codebase -v
```

## Usage

### Command Line Interface

```bash
python main.py <codebase_path> [output_directory] [options]
```

**Arguments:**
- `codebase_path`: Path to the Python codebase to analyze (required)
- `output_directory`: Output directory for the course (default: ./course-output)

**Options:**
- `--verbose`, `-v`: Enable verbose output
- `--help`, `-h`: Show help message

### Examples

```bash
# Analyze a simple project
python main.py ./my-simple-project

# Analyze a complex project with custom output
python main.py /path/to/complex-app ./complex-app-course

# Get verbose output for debugging
python main.py ./my-project -v
```

## Output Structure

The generated course has the following structure:

```
course-output/
├── styles.css          # CSS styles (simplified version)
├── main.js             # JavaScript for interactivity
├── _base.html          # Base HTML template
├── _footer.html        # Footer HTML
├── build.sh            # Build script
├── modules/
│   ├── 01-introduction.html
│   ├── 02-architecture.html
│   ├── 03-components.html
│   ├── 04-data-flow.html
│   └── 05-interactive.html
└── index.html          # Assembled course (open this in your browser)
```

## Course Content

### Module 1: Introduction
- Overview of the codebase
- Project statistics and structure
- Key file types and directories

### Module 2: Architecture
- Main components and their relationships
- Code organization patterns
- Design principles used

### Module 3: Components
- Deep dive into key classes
- Method responsibilities
- Component interactions

### Module 4: Data Flow
- How data moves through the system
- Request/response patterns
- Data processing pipelines

### Module 5: Interactive Elements
- Key functions and their usage
- Code examples with explanations
- Practical applications

## Customization

### Modifying the Course

The generated course is fully customizable:

1. **Edit HTML files**: Modify content in the `modules/` directory
2. **Update styles**: Edit `styles.css` to change colors, fonts, or layout
3. **Add interactivity**: Modify `main.js` to add new interactive elements
4. **Rebuild the course**: Run `bash build.sh` to regenerate `index.html`

### Changing Accent Colors

In `_base.html`, modify the CSS custom properties:

```css
:root {
  --color-accent: #D94F30;        /* Main accent color */
  --color-accent-hover: #C4432A;  /* Hover state */
  --color-accent-light: #FDEEE9;  /* Light background */
  --color-accent-muted: #E8836C;  /* Muted version */
}
```

### Available Color Palettes
- **Vermillion** (default): `#D94F30 / #C4432A / #FDEEE9 / #E8836C`
- **Coral**: `#E06B56 / #C85A47 / #FDECEA / #E89585`
- **Teal**: `#2A7B9B / #1F6280 / #E4F2F7 / #5A9DB8`
- **Amber**: `#D4A843 / #BF9530 / #FDF5E0 / #E0C070`
- **Forest**: `#2D8B55 / #226B41 / #E8F5EE / #5AAD7A`

## Limitations

This is a simplified version with the following limitations:

1. **Python only**: Only analyzes Python files (not JavaScript, TypeScript, etc.)
2. **Basic analysis**: Uses simple AST parsing, not deep semantic analysis
3. **Fixed course structure**: Always generates 5 modules regardless of codebase complexity
4. **Limited interactivity**: Only includes basic quizzes and translation blocks
5. **No AI integration**: Doesn't use AI for content generation

## Comparison with Original

| Feature | Original Skill | This Simplified Version |
|---------|----------------|------------------------|
| Language support | All languages | Python only |
| AI-powered analysis | Yes | No |
| Custom course structure | Dynamic | Fixed 5 modules |
| Interactive elements | Full suite | Basic quizzes |
| Content generation | AI-written | Template-based |
| Deployment | Single HTML file | Directory with files |

## Troubleshooting

### Common Issues

**"No Python files found"**
- Ensure the path points to a directory containing `.py` files
- Check that the path is correct and accessible

**"Error analyzing file"**
- Some Python files may have syntax errors
- The analyzer will skip problematic files and continue

**"Course looks broken"**
- Ensure you're opening `index.html` in a modern browser
- Check that all files were generated correctly

### Debug Mode

Run with verbose output for more information:

```bash
python main.py ./my-project -v
```

## Contributing

This is a simplified demonstration version. For the full-featured original, please visit the [original repository](https://github.com/user/codebase-to-course).

### Potential Improvements

1. **Multi-language support**: Add support for JavaScript, TypeScript, etc.
2. **Better analysis**: Implement deeper code analysis
3. **Dynamic course structure**: Adapt modules based on codebase complexity
4. **More interactive elements**: Add drag-and-drop, animations, etc.
5. **AI integration**: Use AI for content generation

## License

This project is provided for educational purposes. The original codebase-to-course skill is subject to its own license.

## Acknowledgments

- Inspired by the original [Codebase-to-Course](https://github.com/user/codebase-to-course) skill
- Design system based on warm, inviting developer notebook aesthetics
- Built with Python standard library (no external dependencies)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the generated course files
3. Examine the source code for customization options

---

**Note**: This is a simplified educational tool. For production use with complex codebases, consider using the full-featured original skill or similar professional tools.
