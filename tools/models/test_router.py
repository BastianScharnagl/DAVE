def test_model_router():
    """Test the ModelRouter with various types of queries."""
    from .models import router
    
    print("Testing Model Router Functionality\n")
    print("=" * 40)
    
    # Test cases for different query types
    test_cases = [
        "Solve this complex physics problem about quantum mechanics",  # Should route to LISA Pro
        "Think step by step about the implications of artificial intelligence on society",  # Should route to LISA Flash
        "Analyze this image and describe what you see",  # Should route to LISA Vision
        "Write a Python function to calculate Fibonacci numbers",  # Should route to LISA CODE-101
        "Create a beautiful landscape image with mountains and a lake",  # Should route to LISA Bildgenerierung
        "Improve this simple prompt for better image generation: 'a cat'"  # Should route to Prompter
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case}")
        response = router.route(test_case)
        print(f"Model used: {response['model']}")
        print(f"Response: {response['response'][:100]}...\n")
    
    # Test explicit model requests
    print("Testing explicit model requests:")
    explicit_tests = [
        "LISA Pro: Explain the theory of relativity",
        "LISA Flash: Analyze this complex philosophical question",
        "LISA Vision: Describe the content of this photo",
        "LISA CODE-101: Fix this JavaScript code",
        "LISA bildgenerierung: Generate an image of a futuristic city"
    ]
    
    for test in explicit_tests:
        print(f"\n{test}")
        response = router.route(test)
        print(f"Model used: {response['model']}")
    
    # Test model capabilities
    print(f"\nAvailable models: {router.get_available_models()}")
    print(f"Model capabilities: {router.get_model_capabilities()}")
    
    return True