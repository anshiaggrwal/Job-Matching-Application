# skill_testing_module.py - FIXED VERSION
"""
Skill Testing Module for Resume Analyzer - Fixed Version
This module provides comprehensive skill validation through dynamic question generation
"""

import streamlit as st
import requests
import json
import random
from typing import List, Dict, Optional
import time

class SkillTester:
    def __init__(self):
        self.api_key = None  # Set your OpenAI API key here
        self.question_cache = {}
        
    def set_api_key(self, api_key: str):
        """Set OpenAI API key for dynamic question generation"""
        self.api_key = api_key
    
    def _get_fallback_questions(self, skill: str, difficulty: str) -> List[Dict]:
        """Comprehensive fallback questions for when APIs are unavailable"""
        
        FALLBACK_QUESTIONS = {
            "python": {
                "easy": [
                    {
                        "question": "Which of the following is the correct way to create a list in Python?",
                        "options": ["list = {1, 2, 3}", "list = [1, 2, 3]", "list = (1, 2, 3)", "list = <1, 2, 3>"],
                        "answer": 1,
                        "explanation": "Square brackets [] are used to create lists in Python."
                    },
                    {
                        "question": "What is the output of print(type([1, 2, 3]))?",
                        "options": ["<class 'tuple'>", "<class 'list'>", "<class 'dict'>", "<class 'set'>"],
                        "answer": 1,
                        "explanation": "The type() function returns <class 'list'> for list objects."
                    },
                    {
                        "question": "Which keyword is used to define a function in Python?",
                        "options": ["function", "def", "define", "func"],
                        "answer": 1,
                        "explanation": "The 'def' keyword is used to define functions in Python."
                    }
                ],
                "medium": [
                    {
                        "question": "What is the difference between append() and extend() methods?",
                        "options": [
                            "No difference",
                            "append() adds single element, extend() adds multiple elements",
                            "extend() is faster than append()",
                            "append() modifies original list, extend() creates new list"
                        ],
                        "answer": 1,
                        "explanation": "append() adds a single element, while extend() adds multiple elements from an iterable."
                    },
                    {
                        "question": "What does the 'with' statement provide in Python?",
                        "options": [
                            "Loop iteration",
                            "Exception handling",
                            "Context management",
                            "Variable declaration"
                        ],
                        "answer": 2,
                        "explanation": "The 'with' statement provides context management for resource handling."
                    },
                    {
                        "question": "What is list comprehension?",
                        "options": [
                            "A way to understand lists",
                            "A concise way to create lists",
                            "A method to compress lists",
                            "A debugging technique"
                        ],
                        "answer": 1,
                        "explanation": "List comprehension provides a concise way to create lists based on existing iterables."
                    }
                ],
                "hard": [
                    {
                        "question": "What is the Global Interpreter Lock (GIL) in Python?",
                        "options": [
                            "A security mechanism",
                            "A mutex that prevents multiple threads from executing Python bytecode simultaneously",
                            "A database connection pool",
                            "A memory management system"
                        ],
                        "answer": 1,
                        "explanation": "GIL is a mutex that prevents multiple threads from executing Python bytecode at once."
                    },
                    {
                        "question": "What is the difference between deep copy and shallow copy?",
                        "options": [
                            "No difference in Python",
                            "Deep copy copies references, shallow copy copies objects",
                            "Shallow copy is always faster",
                            "Deep copy recursively copies nested objects, shallow copy doesn't"
                        ],
                        "answer": 3,
                        "explanation": "Deep copy creates independent copies of nested objects, shallow copy only copies references."
                    },
                    {
                        "question": "What are Python decorators?",
                        "options": [
                            "Design patterns for classes",
                            "Functions that modify or extend other functions",
                            "Data structures for storing metadata",
                            "Built-in Python libraries"
                        ],
                        "answer": 1,
                        "explanation": "Decorators are functions that modify or extend the behavior of other functions."
                    }
                ]
            },
            "javascript": {
                "easy": [
                    {
                        "question": "What is the correct way to declare a variable in JavaScript?",
                        "options": ["variable x", "var x", "declare x", "v x"],
                        "answer": 1,
                        "explanation": "'var' is one of the keywords used to declare variables in JavaScript."
                    },
                    {
                        "question": "Which method adds an element to the end of an array?",
                        "options": ["add()", "append()", "push()", "insert()"],
                        "answer": 2,
                        "explanation": "The push() method adds elements to the end of an array."
                    },
                    {
                        "question": "What does the '===' operator do?",
                        "options": ["Assigns value", "Compares value only", "Compares value and type", "Creates object"],
                        "answer": 2,
                        "explanation": "The '===' operator compares both value and type (strict equality)."
                    }
                ],
                "medium": [
                    {
                        "question": "What is the main difference between let, const, and var?",
                        "options": [
                            "No significant difference",
                            "Different scoping rules and mutability",
                            "Different syntax only",
                            "Different performance characteristics"
                        ],
                        "answer": 1,
                        "explanation": "let and const have block scope and const is immutable, while var has function scope."
                    },
                    {
                        "question": "What is a closure in JavaScript?",
                        "options": [
                            "A loop construct",
                            "A function that has access to variables in its outer scope",
                            "An object property",
                            "A method definition"
                        ],
                        "answer": 1,
                        "explanation": "A closure is a function that retains access to variables from its outer/enclosing scope."
                    },
                    {
                        "question": "What does the 'this' keyword refer to?",
                        "options": [
                            "The current function",
                            "The global object",
                            "Depends on how the function is called",
                            "The previous object"
                        ],
                        "answer": 2,
                        "explanation": "The value of 'this' depends on the execution context and how the function is invoked."
                    }
                ],
                "hard": [
                    {
                        "question": "What is the Event Loop in JavaScript?",
                        "options": [
                            "A for loop construct",
                            "A mechanism for handling asynchronous operations in single-threaded environment",
                            "A design pattern",
                            "A framework feature"
                        ],
                        "answer": 1,
                        "explanation": "The Event Loop manages asynchronous operations in JavaScript's single-threaded environment."
                    },
                    {
                        "question": "What's the difference between Promise.all() and Promise.allSettled()?",
                        "options": [
                            "No difference",
                            "Promise.all() fails fast, Promise.allSettled() waits for all to complete",
                            "Different syntax only",
                            "Promise.allSettled() is faster"
                        ],
                        "answer": 1,
                        "explanation": "Promise.all() rejects immediately if any promise rejects, while allSettled() waits for all."
                    },
                    {
                        "question": "What is prototypal inheritance?",
                        "options": [
                            "Class-based inheritance like Java",
                            "Objects can inherit directly from other objects",
                            "No inheritance in JavaScript",
                            "Multiple inheritance system"
                        ],
                        "answer": 1,
                        "explanation": "JavaScript uses prototypal inheritance where objects inherit directly from other objects."
                    }
                ]
            },
            "react": {
                "easy": [
                    {
                        "question": "What is JSX in React?",
                        "options": ["JavaScript Extension", "Java Syntax Extension", "JavaScript XML", "JSON Extended"],
                        "answer": 2,
                        "explanation": "JSX stands for JavaScript XML and allows writing HTML-like syntax in JavaScript."
                    },
                    {
                        "question": "How do you create a React component?",
                        "options": ["function Component()", "class Component extends React.Component", "Both A and B", "createComponent()"],
                        "answer": 2,
                        "explanation": "React components can be created as functions or ES6 classes."
                    },
                    {
                        "question": "What is the virtual DOM?",
                        "options": ["The real DOM", "A backup DOM", "A JavaScript representation of the DOM", "A server-side DOM"],
                        "answer": 2,
                        "explanation": "The virtual DOM is a JavaScript representation of the actual DOM kept in memory."
                    }
                ],
                "medium": [
                    {
                        "question": "What are React hooks?",
                        "options": [
                            "Event handlers",
                            "Functions that let you use state and lifecycle features in functional components",
                            "CSS styling methods",
                            "API endpoints"
                        ],
                        "answer": 1,
                        "explanation": "Hooks allow functional components to use state and lifecycle features."
                    },
                    {
                        "question": "When should you use useEffect?",
                        "options": [
                            "For state management only",
                            "For handling side effects",
                            "For styling components",
                            "For routing"
                        ],
                        "answer": 1,
                        "explanation": "useEffect is used for side effects like API calls, subscriptions, or manual DOM changes."
                    },
                    {
                        "question": "What is prop drilling?",
                        "options": [
                            "Creating new props",
                            "Passing props through multiple component levels",
                            "Deleting props",
                            "Updating props dynamically"
                        ],
                        "answer": 1,
                        "explanation": "Prop drilling is passing props through multiple component levels to reach a deeply nested component."
                    }
                ],
                "hard": [
                    {
                        "question": "What's the difference between useMemo and useCallback?",
                        "options": [
                            "No difference",
                            "useMemo memoizes values, useCallback memoizes functions",
                            "Different syntax only",
                            "useCallback is faster"
                        ],
                        "answer": 1,
                        "explanation": "useMemo memoizes computed values, useCallback memoizes function references."
                    },
                    {
                        "question": "How does React's reconciliation work?",
                        "options": [
                            "Compares entire DOM tree",
                            "Uses diffing algorithm on Virtual DOM tree",
                            "Refreshes the entire page",
                            "Uses server-side rendering"
                        ],
                        "answer": 1,
                        "explanation": "React uses a diffing algorithm to compare Virtual DOM trees and update only changed elements."
                    },
                    {
                        "question": "What are Higher Order Components (HOCs)?",
                        "options": [
                            "Large, complex components",
                            "Functions that take a component and return a new component",
                            "Built-in React hooks",
                            "CSS-in-JS solutions"
                        ],
                        "answer": 1,
                        "explanation": "HOCs are functions that take a component and return a new component with additional props or behavior."
                    }
                ]
            },
            "java": {
                "easy": [
                    {
                        "question": "Which keyword is used to create a class in Java?",
                        "options": ["create", "class", "new", "define"],
                        "answer": 1,
                        "explanation": "The 'class' keyword is used to define a class in Java."
                    },
                    {
                        "question": "What is the correct main method signature?",
                        "options": [
                            "public static void main(String args[])",
                            "main(String args[])",
                            "public main()",
                            "static main()"
                        ],
                        "answer": 0,
                        "explanation": "The main method must be public, static, void, and take String array as parameter."
                    },
                    {
                        "question": "Which data type stores whole numbers?",
                        "options": ["float", "double", "int", "char"],
                        "answer": 2,
                        "explanation": "The 'int' data type is used to store whole numbers (integers) in Java."
                    }
                ],
                "medium": [
                    {
                        "question": "What is inheritance in Java?",
                        "options": [
                            "Creating multiple objects",
                            "A class acquiring properties and methods of another class",
                            "Deleting unused classes",
                            "Combining multiple classes into one"
                        ],
                        "answer": 1,
                        "explanation": "Inheritance allows a class to inherit properties and methods from another class."
                    },
                    {
                        "question": "What's the difference between == and .equals()?",
                        "options": [
                            "No difference",
                            "== compares references, .equals() compares content",
                            ".equals() is always faster",
                            "== is deprecated"
                        ],
                        "answer": 1,
                        "explanation": "== compares object references, while .equals() compares object content."
                    },
                    {
                        "question": "What is polymorphism?",
                        "options": [
                            "Having multiple classes",
                            "Same interface with different implementations",
                            "Class inheritance only",
                            "Object creation process"
                        ],
                        "answer": 1,
                        "explanation": "Polymorphism allows objects of different types to be treated as objects of a common base type."
                    }
                ],
                "hard": [
                    {
                        "question": "What is the Java Memory Model?",
                        "options": [
                            "A storage allocation system",
                            "Defines how threads interact through memory and what behaviors are allowed",
                            "A database design pattern",
                            "A file system specification"
                        ],
                        "answer": 1,
                        "explanation": "JMM defines the rules for how threads interact through memory and ensures memory consistency."
                    },
                    {
                        "question": "What are Java 8 Streams?",
                        "options": [
                            "File input/output streams",
                            "Functional-style operations on collections of objects",
                            "Network data streams",
                            "Audio/video streams"
                        ],
                        "answer": 1,
                        "explanation": "Java 8 Streams provide functional-style operations for processing collections of objects."
                    },
                    {
                        "question": "ArrayList vs LinkedList - key difference?",
                        "options": [
                            "No significant difference",
                            "ArrayList uses dynamic arrays, LinkedList uses doubly-linked nodes",
                            "LinkedList is always faster",
                            "ArrayList is deprecated"
                        ],
                        "answer": 1,
                        "explanation": "ArrayList uses resizable arrays while LinkedList uses doubly-linked list structure."
                    }
                ]
            },
            "sql": {
                "easy": [
                    {
                        "question": "Which command retrieves data from a database?",
                        "options": ["GET", "FETCH", "SELECT", "RETRIEVE"],
                        "answer": 2,
                        "explanation": "The SELECT statement is used to query and retrieve data from database tables."
                    },
                    {
                        "question": "What does SQL stand for?",
                        "options": [
                            "Structured Query Language",
                            "Simple Query Language", 
                            "Standard Query Language",
                            "System Query Language"
                        ],
                        "answer": 0,
                        "explanation": "SQL stands for Structured Query Language."
                    },
                    {
                        "question": "Which clause filters rows in a SELECT statement?",
                        "options": ["FILTER", "WHERE", "HAVING", "CONDITION"],
                        "answer": 1,
                        "explanation": "The WHERE clause is used to filter rows based on specified conditions."
                    }
                ],
                "medium": [
                    {
                        "question": "What's the difference between WHERE and HAVING?",
                        "options": [
                            "No difference",
                            "WHERE filters rows, HAVING filters groups",
                            "HAVING is faster than WHERE",
                            "WHERE is deprecated"
                        ],
                        "answer": 1,
                        "explanation": "WHERE filters individual rows, HAVING filters grouped results after GROUP BY."
                    },
                    {
                        "question": "What does JOIN do in SQL?",
                        "options": [
                            "Combines data from multiple tables",
                            "Splits tables into smaller ones",
                            "Creates new tables",
                            "Deletes table data"
                        ],
                        "answer": 0,
                        "explanation": "JOIN operations combine rows from multiple tables based on related columns."
                    },
                    {
                        "question": "What is a primary key?",
                        "options": [
                            "The first column in a table",
                            "A unique identifier for each row",
                            "A foreign key reference",
                            "An index on the table"
                        ],
                        "answer": 1,
                        "explanation": "A primary key uniquely identifies each row in a table and cannot contain NULL values."
                    }
                ],
                "hard": [
                    {
                        "question": "INNER JOIN vs LEFT JOIN - what's the difference?",
                        "options": [
                            "No difference",
                            "INNER returns only matching rows, LEFT returns all left table rows",
                            "LEFT JOIN is always faster",
                            "INNER JOIN is deprecated"
                        ],
                        "answer": 1,
                        "explanation": "INNER JOIN returns only matching rows, LEFT JOIN returns all rows from left table plus matches."
                    },
                    {
                        "question": "What is database normalization?",
                        "options": [
                            "Sorting data alphabetically",
                            "Organizing data to reduce redundancy and dependency",
                            "Creating backup copies",
                            "Indexing all columns"
                        ],
                        "answer": 1,
                        "explanation": "Normalization organizes database structure to minimize redundancy and dependency issues."
                    },
                    {
                        "question": "What are window functions in SQL?",
                        "options": [
                            "Functions for creating GUI windows",
                            "Functions that perform calculations across a set of rows related to current row",
                            "System administration functions",
                            "Database backup functions"
                        ],
                        "answer": 1,
                        "explanation": "Window functions perform calculations across a set of rows that are related to the current row."
                    }
                ]
            },
            "aws": {
                "easy": [
                    {
                        "question": "What does AWS stand for?",
                        "options": [
                            "Amazon Web Services",
                            "Amazon World Services",
                            "Advanced Web Services",
                            "Automated Web Services"
                        ],
                        "answer": 0,
                        "explanation": "AWS stands for Amazon Web Services, Amazon's cloud computing platform."
                    },
                    {
                        "question": "Which service provides object storage?",
                        "options": ["EC2", "S3", "RDS", "Lambda"],
                        "answer": 1,
                        "explanation": "Amazon S3 (Simple Storage Service) provides scalable object storage."
                    },
                    {
                        "question": "What is Amazon EC2?",
                        "options": [
                            "Database service",
                            "Storage service", 
                            "Elastic Compute Cloud - virtual servers",
                            "Network service"
                        ],
                        "answer": 2,
                        "explanation": "EC2 (Elastic Compute Cloud) provides resizable virtual servers in the cloud."
                    }
                ],
                "medium": [
                    {
                        "question": "What's the difference between S3 and EBS?",
                        "options": [
                            "No difference",
                            "S3 is object storage, EBS is block storage",
                            "EBS is cheaper than S3",
                            "S3 is faster than EBS"
                        ],
                        "answer": 1,
                        "explanation": "S3 provides object storage for files, EBS provides block storage volumes for EC2 instances."
                    },
                    {
                        "question": "What is AWS Lambda?",
                        "options": [
                            "Database service",
                            "Serverless compute service",
                            "Storage service",
                            "Network load balancer"
                        ],
                        "answer": 1,
                        "explanation": "Lambda is a serverless compute service that runs code without provisioning servers."
                    },
                    {
                        "question": "What does VPC stand for?",
                        "options": [
                            "Virtual Private Cloud",
                            "Very Private Cloud",
                            "Virtual Public Cloud",
                            "Variable Private Cloud"
                        ],
                        "answer": 0,
                        "explanation": "VPC (Virtual Private Cloud) provides isolated network environments in AWS."
                    }
                ],
                "hard": [
                    {
                        "question": "Application Load Balancer vs Network Load Balancer?",
                        "options": [
                            "No difference",
                            "ALB operates at Layer 7 (HTTP), NLB at Layer 4 (TCP)",
                            "NLB is always cheaper",
                            "ALB is faster than NLB"
                        ],
                        "answer": 1,
                        "explanation": "ALB works at application layer (Layer 7), NLB at transport layer (Layer 4)."
                    },
                    {
                        "question": "What is AWS CloudFormation?",
                        "options": [
                            "Monitoring service",
                            "Infrastructure as Code service for provisioning AWS resources",
                            "Database service",
                            "Content delivery network"
                        ],
                        "answer": 1,
                        "explanation": "CloudFormation allows you to define AWS infrastructure using code templates."
                    },
                    {
                        "question": "What is eventual consistency in DynamoDB?",
                        "options": [
                            "Data is immediately consistent",
                            "Data will become consistent across all nodes eventually",
                            "No consistency guarantees",
                            "Strong consistency always"
                        ],
                        "answer": 1,
                        "explanation": "Eventual consistency means all replicas will eventually have the same data, but not immediately."
                    }
                ]
            }
        }
        
        skill_lower = skill.lower()
        if skill_lower in FALLBACK_QUESTIONS and difficulty in FALLBACK_QUESTIONS[skill_lower]:
            return FALLBACK_QUESTIONS[skill_lower][difficulty]
        
        # Generic fallback for unknown skills
        return [
            {
                "question": f"What is the primary use of {skill}?",
                "options": [
                    f"{skill} is used for web development",
                    f"{skill} is used for data analysis", 
                    f"{skill} is used for system administration",
                    "All of the above depending on context"
                ],
                "answer": 3,
                "explanation": f"The usage of {skill} depends on the specific context and requirements."
            }
        ]
    
    def conduct_skill_assessment(self, skills: List[str]) -> Dict:
        """Main function to conduct comprehensive skill assessment"""
        st.title("🎯 Skill Validation Assessment")
        st.markdown("Test your knowledge on the skills extracted from your resume!")
        
        if not skills:
            st.warning("No skills found to test. Please upload and analyze your resume first.")
            return {}
        
        # Initialize session state for testing
        if 'current_test_skill' not in st.session_state:
            st.session_state.current_test_skill = None
        if 'current_test_difficulty' not in st.session_state:
            st.session_state.current_test_difficulty = None
        if 'current_questions' not in st.session_state:
            st.session_state.current_questions = []
        if 'current_answers' not in st.session_state:
            st.session_state.current_answers = {}
        if 'test_completed' not in st.session_state:
            st.session_state.test_completed = False
        if 'test_results' not in st.session_state:
            st.session_state.test_results = {}
        
        # Skill selection
        st.subheader("📋 Select Skills to Test")
        
        # Limit to reasonable number of skills for testing
        available_skills = skills[:15]  # Test max 15 skills
        
        selected_skill = st.selectbox(
            "Choose skill you want to be tested on:",
            [''] + available_skills,
            help="Select the skill you want to validate through testing"
        )
        
        if not selected_skill:
            st.info("Please select a skill to test.")
            return {}
        
        # Difficulty selection
        difficulty_level = st.selectbox(
            "Choose difficulty level:",
            ["easy", "medium", "hard"],
            index=1,  # Default to medium
            help="Select the difficulty level for your test questions"
        )
        
        # Start new test button
        if st.button("🚀 Start New Test", type="primary"):
            # Reset test state
            st.session_state.current_test_skill = selected_skill
            st.session_state.current_test_difficulty = difficulty_level
            st.session_state.current_questions = self._get_fallback_questions(selected_skill, difficulty_level)
            st.session_state.current_answers = {}
            st.session_state.test_completed = False
            st.rerun()
        
        # Display current test if one is active
        if st.session_state.current_test_skill and st.session_state.current_questions:
            self._display_current_test()
        
        return st.session_state.test_results
    
    def _display_current_test(self):
        """Display the current active test"""
        skill = st.session_state.current_test_skill
        difficulty = st.session_state.current_test_difficulty
        questions = st.session_state.current_questions
        
        st.markdown("---")
        st.subheader(f"🔍 Testing: {skill.title()} ({difficulty.title()} Level)")
        
        # Progress indicator
        answered_count = len(st.session_state.current_answers)
        total_questions = len(questions)
        
        progress = answered_count / total_questions if total_questions > 0 else 0
        st.progress(progress)
        st.write(f"Progress: {answered_count}/{total_questions} questions answered")
        
        # Display questions
        all_answered = True
        for i, question in enumerate(questions):
            st.markdown(f"**Question {i+1}:** {question['question']}")
            
            # Create unique key for each question
            question_key = f"test_{skill}_{difficulty}_q{i}"
            
            # Check if this question was already answered
            current_answer = st.session_state.current_answers.get(question_key, None)
            
            selected_answer = st.radio(
                "Choose your answer:",
                question['options'],
                key=question_key,
                index=current_answer if current_answer is not None else None
            )
            
            # Store the answer when selected
            if selected_answer is not None:
                answer_index = question['options'].index(selected_answer)
                st.session_state.current_answers[question_key] = answer_index
                
                # Show immediate feedback
                is_correct = answer_index == question['answer']
                if is_correct:
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Incorrect. The correct answer is: {question['options'][question['answer']]}")
                
                if question.get('explanation'):
                    st.info(f"💡 **Explanation:** {question['explanation']}")
            else:
                all_answered = False
            
            st.markdown("---")
        
        # Submit test button
        if all_answered and not st.session_state.test_completed:
            if st.button("📊 Submit Test", type="primary"):
                self._calculate_and_store_results()
                st.session_state.test_completed = True
                st.success("Test completed! Check the Results tab to see your score.")
                st.rerun()
        
        # Show completion message
        if st.session_state.test_completed:
            st.success("✅ Test completed! Your results have been saved.")
            if st.button("🔄 Take Another Test"):
                # Reset for new test
                st.session_state.current_test_skill = None
                st.session_state.current_test_difficulty = None
                st.session_state.current_questions = []
                st.session_state.current_answers = {}
                st.session_state.test_completed = False
                st.rerun()
    
    def _calculate_and_store_results(self):
        """Calculate test results and store them"""
        skill = st.session_state.current_test_skill
        difficulty = st.session_state.current_test_difficulty
        questions = st.session_state.current_questions
        answers = st.session_state.current_answers
        
        correct_count = 0
        detailed_answers = []
        
        for i, question in enumerate(questions):
            question_key = f"test_{skill}_{difficulty}_q{i}"
            user_answer_index = answers.get(question_key, -1)
            
            if user_answer_index >= 0:
                is_correct = user_answer_index == question['answer']
                if is_correct:
                    correct_count += 1
                
                detailed_answers.append({
                    'question': question['question'],
                    'user_answer': question['options'][user_answer_index],
                    'correct_answer': question['options'][question['answer']],
                    'is_correct': is_correct,
                    'explanation': question.get('explanation', '')
                })
        
        total_questions = len(questions)
        percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
        
        # Store results
        result_key = f"{skill}_{difficulty}"
        st.session_state.test_results[result_key] = {
            'skill': skill,
            'difficulty': difficulty,
            'score': correct_count,
            'total': total_questions,
            'percentage': percentage,
            'answers': detailed_answers,
            'status': self._get_skill_status(percentage),
            'timestamp': time.time()
        }
    
    def _get_skill_status(self, percentage: float) -> str:
        """Get skill validation status based on score"""
        if percentage >= 80:
            return "Expert ⭐⭐⭐"
        elif percentage >= 60:
            return "Proficient ⭐⭐"
        elif percentage >= 40:
            return "Beginner ⭐"
        else:
            return "Needs Improvement ❌"

# Streamlit integration functions for easy integration with existing app
def add_skill_testing_tab(skills: List[str]):
    """Add skill testing functionality as a Streamlit tab"""
    tester = SkillTester()
    
    # Initialize test results in session state if not exists
    if 'test_results' not in st.session_state:
        st.session_state.test_results = {}
    
    results = tester.conduct_skill_assessment(skills)
    
    return results

def create_skill_testing_sidebar(skills: List[str]):
    """Create a sidebar widget for quick skill testing"""
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🎯 Quick Skill Test")
        
        if skills:
            test_skill = st.selectbox("Select skill to test:", [''] + skills)
            test_difficulty = st.selectbox("Difficulty:", ["easy", "medium", "hard"])
            
            if test_skill and st.button("Start Quick Test"):
                tester = SkillTester()
                questions = tester._get_fallback_questions(test_skill, test_difficulty)
                
                if questions:
                    st.markdown(f"**Testing {test_skill} - {test_difficulty}**")
                    # This would need additional implementation for sidebar testing
                    st.info("Full test available in Skill Testing tab!")

def display_test_results():
    """Display comprehensive test results"""
    if 'test_results' not in st.session_state or not st.session_state.test_results:
        st.info("🎯 No test results yet! Complete a skill test to see your results here.")
        st.markdown("### How to get results:")
        st.markdown("1. Analyze your resume in the first tab")
        st.markdown("2. Take skill tests in the second tab")
        st.markdown("3. View your detailed results here!")
        return
    
    results = st.session_state.test_results
    st.subheader("📊 Your Skill Assessment Results")
    
    # Overall statistics
    total_tests = len(results)
    if total_tests > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Tests Completed", total_tests)
        with col2:
            avg_score = sum(r.get('percentage', 0) for r in results.values()) / total_tests
            st.metric("Average Score", f"{avg_score:.1f}%")
        with col3:
            expert_skills = sum(1 for r in results.values() if r.get('percentage', 0) >= 80)
            st.metric("Expert Level", expert_skills)
        with col4:
            total_questions = sum(r.get('total', 0) for r in results.values())
            st.metric("Questions Answered", total_questions)
        
        st.markdown("---")
        
        # Individual skill results
        st.subheader("🎯 Individual Test Results")
        
        for test_key, result in results.items():
            skill = result.get('skill', 'Unknown')
            difficulty = result.get('difficulty', 'Unknown')
            percentage = result.get('percentage', 0)
            status = result.get('status', 'Unknown')
            
            # Create expandable section for each test
            with st.expander(f"{skill.title()} ({difficulty}) - {percentage:.1f}% ({status})"):
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Score", f"{result.get('score', 0)}/{result.get('total', 0)}")
                with col2:
                    st.metric("Percentage", f"{percentage:.1f}%")
                with col3:
                    st.metric("Status", status)
                
                # Detailed answers
                answers = result.get('answers', [])
                if answers:
                    st.markdown("**📋 Question-by-Question Results:**")
                    
                    correct_count = 0
                    for i, answer in enumerate(answers):
                        if answer['is_correct']:
                            correct_count += 1
                            st.success(f"✅ **Q{i+1}:** Correct")
                        else:
                            st.error(f"❌ **Q{i+1}:** Incorrect")
                            
                        # Show details in a compact format
                        with st.container():
                            st.markdown(f"**Question:** {answer['question']}")
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.markdown(f"**Your answer:** {answer['user_answer']}")
                            with col_b:
                                st.markdown(f"**Correct answer:** {answer['correct_answer']}")
                            
                            if answer.get('explanation'):
                                st.info(f"💡 {answer['explanation']}")
                        
                        st.markdown("---")
        
        # Recommendations based on results
        st.subheader("💡 Recommendations")
        
        weak_skills = []
        strong_skills = []
        
        for result in results.values():
            skill = result.get('skill', '')
            percentage = result.get('percentage', 0)
            if percentage < 60:
                weak_skills.append(skill)
            elif percentage >= 80:
                strong_skills.append(skill)
        
        if weak_skills:
            st.warning("**Skills needing improvement:**")
            for skill in set(weak_skills):  # Remove duplicates
                st.markdown(f"- **{skill}:** Consider reviewing fundamentals and practicing more")
        
        if strong_skills:
            st.success("**Strong skills validated:**")
            for skill in set(strong_skills):  # Remove duplicates
                st.markdown(f"- **{skill}:** Excellent knowledge demonstrated!")
        
        # Export functionality
        st.subheader("📄 Export Results")
        
        if st.button("💾 Download Results as JSON"):
            import json
            
            # Prepare results for export
            export_data = {
                'summary': {
                    'total_tests': total_tests,
                    'average_score': avg_score,
                    'expert_skills': expert_skills,
                    'total_questions': total_questions
                },
                'detailed_results': results,
                'export_timestamp': time.time()
            }
            
            results_json = json.dumps(export_data, indent=2, default=str)
            st.download_button(
                label="📥 Download Results",
                data=results_json,
                file_name=f"skill_assessment_results_{int(time.time())}.json",
                mime="application/json"
            )
        
        # Clear results option
        if st.button("🗑️ Clear All Results", type="secondary"):
            st.session_state.test_results = {}
            st.success("All test results cleared!")
            st.rerun()

# Example usage and integration guide
def example_integration():
    """
    Example of how to integrate this testing module with your existing resume analyzer.
    
    Add this to your main app:
    
    ```python
    import skill_testing_module as stm
    
    # After extracting skills from resume:
    if skills:
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["Resume Analysis", "Skill Testing", "Test Results"])
        
        with tab1:
            # Your existing resume analysis code
            pass
            
        with tab2:
            if st.session_state.get('extracted_skills'):
                stm.add_skill_testing_tab(st.session_state.extracted_skills)
            else:
                st.info("Please analyze your resume first!")
            
        with tab3:
            stm.display_test_results()
    ```
    """
    pass

if __name__ == "__main__":
    # Demo mode
    st.title("🎯 Skill Testing Module Demo")
    
    demo_skills = ["python", "javascript", "react", "sql", "aws"]
    
    st.markdown("This is a standalone demo of the Skill Testing Module.")
    st.markdown("**Available Skills for Testing:**")
    for skill in demo_skills:
        st.markdown(f"- {skill}")
    
    tab1, tab2 = st.tabs(["🎯 Take Test", "📊 View Results"])
    
    with tab1:
        tester = SkillTester()
        tester.conduct_skill_assessment(demo_skills)
    
    with tab2:
        stm.display_test_results()