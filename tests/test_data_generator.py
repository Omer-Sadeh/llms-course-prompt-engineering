from src.utils.data_generator import SyllogismGenerator


def test_dataset_structure():
    gen = SyllogismGenerator(seed=42)
    dataset = gen.generate_dataset(size=10)
    
    assert len(dataset) == 10
    for item in dataset:
        assert 'question' in item
        assert 'answer' in item
        assert 'label' in item
        assert item['label'] in ['Yes', 'No']

def test_valid_syllogism_format():
    gen = SyllogismGenerator()
    item = gen.generate_valid_syllogism()
    assert "Premise 1" in item['question']
    assert "Premise 2" in item['question']
    assert "Question" in item['question']
    assert item['label'] == "Yes"

def test_invalid_syllogism_format():
    gen = SyllogismGenerator()
    item = gen.generate_invalid_syllogism()
    assert item['label'] == "No"
