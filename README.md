# engagement_detector

## Proposed tools:
- CV2 (opencv, for simple CV tasks)
- Keras (for CNNs, may change after research for existing models)
- pytest (Testing)
- pyqt (GUI)

## Git:
- main (only merge into after review/testing)
- develop (checkout new feature-branches from here, implement and merge back)
- feature branches
- release
(- hotfixes)
-> siehe Git-flow: https://datasift.github.io/gitflow/IntroducingGitFlow.html

## Codestyle: 
- PEP-8
- docstring-style: google:

```python
def f(a: int, b: float) -> int:  
    """do stuff  
 
    Args:  
        a (int): is an int  
        b (float): this is a float  
  
    Returns:  
        int: its just a 0  
    """  
    return 0
```