def test_generate_interaction_filename(freezer):
    # Freeze time to 2024-01-01 12:34:56
    freezer.move_to('2024-01-01 12:34:56')
    
    # Test basic filename generation
    filename = generate_interaction_filename("observe")
    assert filename == "240101_123456-observe.md"
    
    # Test filename with perspective
    filename = generate_interaction_filename("consult", "Test Perspective")
    assert filename == "240101_123456-consult_Test_Perspective.md"
