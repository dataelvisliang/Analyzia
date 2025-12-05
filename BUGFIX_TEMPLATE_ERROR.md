# Bug Fix: Template KeyError

## Problem

When starting the application, a KeyError occurred:

```
KeyError: "'the', 'and', 'to', 'of', 'a', 'in', 'is', 'it', 'for', 'this', 'that'"

File "src/agents/data_analysis_agent.py", line 27, in setup_agent
    system_prompt = SYSTEM_TEMPLATE.format(df_schema=df_schema)
```

## Root Cause

**Location**: `src/config/prompts.py:47`

**Issue**: The system prompt template contained a Python set literal with curly braces:

```python
stopwords = {'the', 'and', 'to', 'of', 'a', 'in', 'is', 'it', 'for', 'this', 'that'}
```

When using `.format()` on this string template, Python interpreted the curly braces `{}` as format placeholders, causing a KeyError.

## Solution

**Escape the curly braces** by doubling them:

**Before**:
```python
stopwords = {'the', 'and', 'to', ...}
```

**After**:
```python
stopwords = {{'the', 'and', 'to', ...}}
```

In Python format strings:
- `{{` becomes `{` after `.format()`
- `}}` becomes `}` after `.format()`

## File Modified

**src/config/prompts.py** (line 47)
- Changed single braces to double braces in set literal

## Technical Details

### Why This Happens

Python's `.format()` method treats anything in curly braces as a placeholder:

```python
# This works
template = "Hello {name}"
result = template.format(name="World")  # "Hello World"

# This fails
template = "Set: {'a', 'b'}"
result = template.format()  # KeyError: 'a', 'b'

# This works - escaped braces
template = "Set: {{'a', 'b'}}"
result = template.format()  # "Set: {'a', 'b'}"
```

### The Fix in Context

```python
SYSTEM_TEMPLATE = """
...
Example 2 - Word frequency:
```python
# Before: This caused KeyError
stopwords = {'the', 'and', 'to', 'of', 'a'}

# After: This works correctly
stopwords = {{'the', 'and', 'to', 'of', 'a'}}
```
...
""".format(df_schema=schema)  # Now this works!
```

## Testing

```bash
# Test the fix
cd "c:\Users\liang\Desktop\ML Notebooks\Analyzia"
python -c "from src.config import SYSTEM_TEMPLATE; test = SYSTEM_TEMPLATE.format(df_schema='test'); print('Success')"
```

**Result**: ✅ No KeyError

## Prevention

### Rule for Template Strings

When writing string templates that will use `.format()`:

1. **Use double braces for literals**:
   - Sets: `{{'item1', 'item2'}}`
   - Dicts: `{{'key': 'value'}}`
   - Any literal curly braces: `{{` and `}}`

2. **Use single braces for placeholders**:
   - `{variable_name}`
   - `{0}`, `{1}` for positional args

### Example

```python
# Template with both placeholders and literals
template = """
Column schema: {schema}

Example code:
my_dict = {{'key': 'value'}}
my_set = {{'a', 'b', 'c'}}
"""

# This works correctly
result = template.format(schema="id, name, age")
```

## Related Documentation

- Python `.format()` docs: https://docs.python.org/3/library/string.html#formatstrings
- String formatting guide: https://peps.python.org/pep-3101/

## Status

✅ **Fixed and Tested**

The application now starts without KeyError and the prompt template works correctly.

## Impact

- **Severity**: High (application wouldn't start)
- **Fix complexity**: Low (single line change)
- **Testing**: Verified with import test
- **User impact**: None (internal fix)

## Lessons Learned

1. Always escape literal braces in format strings
2. Test template formatting before using in production
3. Consider using f-strings or other formatting methods if templates become complex
4. Document template string requirements clearly

---

**Fixed**: 2025-12-04
**Severity**: High → Low (fixed)
**Status**: ✅ Resolved
