"""
Demo script for AI Tutor Orchestrator
This script demonstrates the system's capabilities with realistic scenarios.
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test if the API is running."""
    try:
        response = requests.get(f"{BASE_URL}/")
        print("✅ API Health Check:", response.json())
        return True
    except requests.exceptions.ConnectionError:
        print("❌ API is not running. Please start the server with: python main.py")
        return False

def demo_note_making():
    """Demo: Student needs notes on a topic."""
    print("\n📝 DEMO 1: Note Making Request")
    print("=" * 50)
    
    request_data = {
        "user_info": {
            "user_id": "student123",
            "name": "Alice",
            "grade_level": "10",
            "learning_style_summary": "Visual learner, prefers structured notes with examples",
            "emotional_state_summary": "Focused and motivated",
            "mastery_level_summary": "Level 6: Good understanding, ready for application"
        },
        "chat_history": [
            {"role": "user", "content": "I'm studying for my biology exam"},
            {"role": "assistant", "content": "What specific topics are you covering?"}
        ],
        "current_message": "I need comprehensive notes on photosynthesis for my biology class"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/orchestrate", json=request_data)
        result = response.json()
        
        if result["success"]:
            print(f"✅ Tool Selected: {result['tool_name']}")
            print(f"📚 Topic: {result['response_data']['topic']}")
            print(f"📖 Title: {result['response_data']['title']}")
            print(f"📝 Summary: {result['response_data']['summary']}")
            print(f"🎯 Note Style: {result['response_data']['note_taking_style']}")
            print(f"🔑 Key Concepts: {', '.join(result['response_data']['key_concepts'])}")
        else:
            print(f"❌ Error: {result['error_message']}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def demo_flashcard_generation():
    """Demo: Student needs practice flashcards."""
    print("\n🃏 DEMO 2: Flashcard Generation")
    print("=" * 50)
    
    request_data = {
        "user_info": {
            "user_id": "student456",
            "name": "Bob",
            "grade_level": "8",
            "learning_style_summary": "Kinesthetic learner, learns best through practice and repetition",
            "emotional_state_summary": "Focused and motivated to improve",
            "mastery_level_summary": "Level 4: Building foundational knowledge"
        },
        "chat_history": [
            {"role": "user", "content": "I'm struggling with math concepts"},
            {"role": "assistant", "content": "Which math topics are giving you trouble?"}
        ],
        "current_message": "I need some practice flashcards for algebra equations to review before my test"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/orchestrate", json=request_data)
        result = response.json()
        
        if result["success"]:
            print(f"✅ Tool Selected: {result['tool_name']}")
            print(f"📚 Topic: {result['response_data']['topic']}")
            print(f"🎯 Difficulty: {result['response_data']['difficulty']}")
            print(f"📊 Number of Cards: {len(result['response_data']['flashcards'])}")
            print(f"🔧 Adaptation: {result['response_data']['adaptation_details']}")
            
            # Show first flashcard as example
            if result['response_data']['flashcards']:
                first_card = result['response_data']['flashcards'][0]
                print(f"\n📋 Sample Flashcard:")
                print(f"   Question: {first_card['question']}")
                print(f"   Answer: {first_card['answer']}")
        else:
            print(f"❌ Error: {result['error_message']}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def demo_concept_explanation():
    """Demo: Student needs concept explanation."""
    print("\n🧠 DEMO 3: Concept Explanation")
    print("=" * 50)
    
    request_data = {
        "user_info": {
            "user_id": "student789",
            "name": "Charlie",
            "grade_level": "7",
            "learning_style_summary": "Auditory learner, prefers simple terms and step-by-step explanations",
            "emotional_state_summary": "Curious and engaged in learning",
            "mastery_level_summary": "Level 3: Building foundational knowledge"
        },
        "chat_history": [
            {"role": "user", "content": "I don't understand how photosynthesis works"},
            {"role": "assistant", "content": "Let me help you understand photosynthesis step by step."}
        ],
        "current_message": "Can you explain photosynthesis in simple terms? I'm really confused about the whole process"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/orchestrate", json=request_data)
        result = response.json()
        
        if result["success"]:
            print(f"✅ Tool Selected: {result['tool_name']}")
            print(f"🧠 Concept: {result['response_data']['explanation'][:100]}...")
            print(f"📚 Examples: {len(result['response_data']['examples'])} provided")
            print(f"🔗 Related Concepts: {', '.join(result['response_data']['related_concepts'])}")
            print(f"🎨 Visual Aids: {', '.join(result['response_data']['visual_aids'])}")
            print(f"❓ Practice Questions: {len(result['response_data']['practice_questions'])} provided")
        else:
            print(f"❌ Error: {result['error_message']}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def demo_direct_tool_calling():
    """Demo: Direct tool calling for testing."""
    print("\n🔧 DEMO 4: Direct Tool Calling")
    print("=" * 50)
    
    # Test direct flashcard generator call
    tool_request = {
        "tool_name": "flashcard_generator",
        "parameters": {
            "user_info": {
                "user_id": "test123",
                "name": "Test Student",
                "grade_level": "9",
                "learning_style_summary": "Visual learner",
                "emotional_state_summary": "Focused",
                "mastery_level_summary": "Level 5: Developing competence"
            },
            "topic": "World War II",
            "count": 3,
            "difficulty": "medium",
            "subject": "History",
            "include_examples": True
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/tools/flashcard_generator", json=tool_request)
        result = response.json()
        
        if result["success"]:
            print(f"✅ Direct Tool Call Successful: {result['tool_name']}")
            print(f"📚 Topic: {result['response_data']['topic']}")
            print(f"📊 Generated {len(result['response_data']['flashcards'])} flashcards")
        else:
            print(f"❌ Error: {result['error_message']}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def list_available_tools():
    """List all available tools."""
    print("\n🛠️  AVAILABLE TOOLS")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/tools")
        tools = response.json()
        
        print("Available Educational Tools:")
        for tool in tools["available_tools"]:
            print(f"  • {tool}")
        
        print(f"\nTool Schemas:")
        for tool_name, schema in tools["tool_schemas"].items():
            print(f"  📋 {tool_name}:")
            print(f"     Required: {', '.join(schema['required'])}")
            if schema['optional']:
                print(f"     Optional: {', '.join(schema['optional'])}")
                
    except Exception as e:
        print(f"❌ Request failed: {e}")

def main():
    """Run all demo scenarios."""
    print("🚀 AI Tutor Orchestrator Demo")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if API is running
    if not test_health():
        return
    
    # Run demos
    list_available_tools()
    demo_note_making()
    demo_flashcard_generation()
    demo_concept_explanation()
    demo_direct_tool_calling()
    
    print("\n✅ Demo completed successfully!")
    print("\n💡 Key Features Demonstrated:")
    print("  • Intelligent parameter extraction from conversation")
    print("  • Automatic tool selection based on context")
    print("  • Adaptive content based on student profile")
    print("  • Robust error handling and validation")
    print("  • Multiple educational tool integration")

if __name__ == "__main__":
    main()
