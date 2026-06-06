def compute_lps_array(pattern: str) -> list[int]:
    """
    Generates the Longest Prefix Suffix (LPS) lookup array for the KMP algorithm.
    Time Complexity: O(M) where M is the pattern length.
    Space Complexity: O(M)
    """
    m = len(pattern)
    lps = [0] * m
    length = 0  # Length of the previous longest prefix suffix
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text: str, pattern: str) -> list[int]:
    """
    Executes a linear-time substring search using the KMP prefix matching technique.
    Time Complexity: O(N + M)
    Space Complexity: O(M)
    """
    if not pattern or not text:
        return []
        
    n = len(text)
    m = len(pattern)
    matches = []
    
    lps = compute_lps_array(pattern)
    i = 0  # Index for text
    j = 0  # Index for pattern
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
            
        if j == m:
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return matches

def rabin_karp_search(text: str, pattern: str, prime: int = 101, modulus: int = 1000000007) -> list[int]:
    """
    Executes a substring search using the Rabin-Karp algorithm with rolling polynomial hashing.
    Time Complexity: O(N + M) average case, O(N * M) worst case.
    Space Complexity: O(1)
    """
    if not pattern or not text:
        return []
        
    n = len(text)
    m = len(pattern)
    
    if m > n:
        return []
        
    matches = []
    alphabet_size = 256
    
    pattern_hash = 0
    text_hash = 0
    hash_multiplier = 1 # Equivalent to (alphabet_size ** (m-1)) % modulus

    # Precompute the multiplier factor for the highest power position
    for i in range(m - 1):
        hash_multiplier = (hash_multiplier * alphabet_size) % modulus

    # Calculate initial hash values for pattern and the first text window
    for i in range(m):
        pattern_hash = (alphabet_size * pattern_hash + ord(pattern[i])) % modulus
        text_hash = (alphabet_size * text_hash + ord(text[i])) % modulus

    # Slide the pattern window across the text row
    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            # Verify actual string equality on hash matches to handle potential collisions
            if text[i : i + m] == pattern:
                matches.append(i)

        # Compute hash value for the next window: remove leading digit, add trailing digit
        if i < n - m:
            text_hash = (alphabet_size * (text_hash - ord(text[i]) * hash_multiplier) + ord(text[i + m])) % modulus
            # Ensure the calculated hash value remains positive
            if text_hash < 0:
                text_hash += modulus
                
    return matches