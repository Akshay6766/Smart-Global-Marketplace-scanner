#!/usr/bin/env python3
"""
Script to enhance error handling in bedrock_ai_assistant.py
"""

def fix_error_handling():
    # Read the original file
    with open('bedrock_ai_assistant.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the error handling section
    old_section = '''        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AccessDeniedException':
                return {
                    "response": "⚠️ Bedrock access denied. Please enable model access in AWS Console.",
                    "suggestions": ["Go to AWS Bedrock Console → Model access → Enable Claude"],
                    "ready_to_search": False
                }
            else:
                return {
                    "response": f"Sorry, I encountered an error: {error_code}",
                    "suggestions": [],
                    "ready_to_search": False
                }
        except Exception as e:
            print(f"Chat error: {e}")
            return {
                "response": "I'm having trouble right now. Could you try rephrasing that?",
                "suggestions": [],
                "ready_to_search": False
            }'''
    
    new_section = '''        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error'].get('Message', 'Unknown error')
            
            # Enhanced logging for debugging
            print(f"[ERROR] Bedrock ClientError:")
            print(f"  Model ID: {self.model_id}")
            print(f"  Error Code: {error_code}")
            print(f"  Error Message: {error_message}")
            print(f"  Region: {self.region}")
            
            if error_code == 'AccessDeniedException':
                return {
                    "response": f"⚠️ Access denied for model {self.model_id}. Please enable this model in AWS Bedrock Console → Model access.",
                    "suggestions": [
                        "Go to AWS Bedrock Console → Model access",
                        f"Enable access for {self.model_id}",
                        "Try switching to Claude Haiku (usually available by default)"
                    ],
                    "ready_to_search": False
                }
            elif error_code == 'ValidationException':
                return {
                    "response": f"⚠️ Model {self.model_id} not available in {self.region}. Try switching models.",
                    "suggestions": [
                        "Switch to Claude Haiku or Claude Sonnet",
                        "Check model availability in your AWS region"
                    ],
                    "ready_to_search": False
                }
            else:
                return {
                    "response": f"Sorry, I encountered an error: {error_code} - {error_message}",
                    "suggestions": ["Try switching to a different AI model"],
                    "ready_to_search": False
                }
        except Exception as e:
            print(f"[ERROR] Chat error: {e}")
            print(f"  Model ID: {self.model_id}")
            return {
                "response": "I'm having trouble right now. Could you try rephrasing that?",
                "suggestions": ["Try switching to a different AI model"],
                "ready_to_search": False
            }'''
    
    # Replace the section
    if old_section in content:
        content = content.replace(old_section, new_section)
        
        # Write back to file
        with open('bedrock_ai_assistant.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✓ Enhanced error handling applied successfully!")
        return True
    else:
        print("✗ Could not find the exact error handling section to replace")
        return False

if __name__ == "__main__":
    fix_error_handling()