# engagement_detector

## Before program starts
- change roots in config.yml in root directory
- disable hardware acceleration for window capture



## Proposed tools:
- Facerecognition Library and PIL
- Keras (for CNNs, may change after research for existing models)
- pytest (Testing)
- TKinter (GUI)

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
