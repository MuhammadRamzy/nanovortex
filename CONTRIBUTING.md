# Contributing to NanoVortex  

Thank you for your interest in contributing to **NanoVortex**! This document outlines the basics of how you can help.  

---

## How to Contribute  

### Reporting Issues  
- Clearly describe the issue and steps to reproduce it.  
- Include screenshots or logs if applicable.  

### Suggesting Enhancements  
- Outline the feature, its purpose, and benefits.  

### Contributing Code  
- Bug fixes, new features, or documentation improvements are welcome.  
- Follow the [Development Workflow](#development-workflow).  

---

## Development Workflow  

1. **Fork and Clone**  
   ```bash  
   git clone https://github.com/MuhammadRamzy/nanovortex.git  
   cd NanoVortex  
   ```  

2. **Set Up Environment**  
   Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. **Create a Branch**  
   ```bash  
   git checkout -b feature/your-feature-name  
   ```  

4. **Make Changes and Test**  
   Add tests for new features and ensure all existing tests pass.  

5. **Commit and Push**  
   Use clear commit messages:  
   ```bash  
   git commit -m "Add: Brief description of change"  
   git push origin feature/your-feature-name  
   ```  

6. **Open a Pull Request**  
   Submit your changes to the `main` branch with a brief description.  

---

## Code Guidelines  

- Follow **PEP 8** for Python code.  
- Use descriptive names and add docstrings for functions and classes.  

Example:  
```python  
def example_function(param):  
    """Describe the function's purpose.  

    Args:  
        param (type): Description.  

    Returns:  
        type: Description.  
    """  
    pass  
```  

---

## Testing  

- Write tests for all new features and bug fixes using `pytest`.  
- Ensure simulations cover edge cases and expected behavior.  

---

Thank you for helping us improve **NanoVortex**!  

---  