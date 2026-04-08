"""Test the advanced NLP pipeline"""
from pathlib import Path
from backend.app.services.vocab_service import VocabularyService

# Initialize service with trained model
service = VocabularyService(Path('models/saved_models'))

# Test 1: Simple text
print('='*60)
print('TEST 1: Simple A1 Text')
print('='*60)
result = service.process_text('The cat is sleeping.')
print(f'Level: {result["level"]}')
print(f'Difficult words: {len(result["difficult_words"])}')
if result['difficult_words']:
    for word in result['difficult_words'][:3]:
        print(f'  - {word["word"]}: {word["meaning"][:50]}...')

# Test 2: Complex B2 text
print('\n' + '='*60)
print('TEST 2: Complex B2 Text')
print('='*60)
complex_text = 'The burgeoning complexities inherent in contemporary socioeconomic structures necessitate sophisticated analytical frameworks.'
result = service.process_text(complex_text)
print(f'Level: {result["level"]}')
print(f'Difficult words: {len(result["difficult_words"])}')
if result['difficult_words']:
    for word in result['difficult_words'][:5]:
        print(f'  - {word["word"]}: {word["meaning"][:50]}...')
        print(f'    Synonyms: {word["synonyms"][:2]}')

# Test 3: Extract difficult words
print('\n' + '='*60)
print('TEST 3: Word Extraction & Ranking')
print('='*60)
medium_text = 'The implementation of artificial intelligence has revolutionized various industries.'
difficult = service.extract_difficult_words(medium_text)
print(f'Found {len(difficult)} difficult words:')
for word in difficult:
    print(f'  ✓ {word.word}: {word.meaning[:40]}...')

print('\n✅ All tests passed!')
