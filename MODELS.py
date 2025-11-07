# ============================================================================
# RESPONSE MODELS - MULTIPLE QUESTION TYPES
# ============================================================================

class MCQOption(BaseModel):
    text: str = Field(description="The text of the option")
    correct: bool = Field(description="Whether this option is correct")

class MCQQuestion(BaseModel):
    question_type: str = Field(default="multiple_choice", description="Always 'mcq'")
    question_text: str = Field(description="The question text")
    options: List[MCQOption] = Field(description="List of 4 answer options")

class FillInBlankQuestion(BaseModel):
    question_type: str = Field(default="fill_in_the_blanks", description="Always 'fill_blank'")
    question_text: str = Field(
        description="Question with _____ for the blank. Example: 'Vector _____ store numerical representations of text.'"
    )
    correct_answer: str = Field(description="The correct word/phrase for the blank")
    distractors: List[str] = Field(
        description="3 plausible wrong answers that could fit the blank"
    )

class TrueFalseQuestion(BaseModel):
    question_type: str = Field(default="true_false", description="Always 'true_false'")
    statement: str = Field(description="A statement that is either true or false")
    correct_answer: bool = Field(description="True or False")
    explanation: str = Field(
        description="Brief explanation (1 sentence) of why it's true/false"
    )

class MatchingPair(BaseModel):
    left: str = Field(description="Left side item (term, concept, etc.)")
    right: str = Field(description="Right side item that matches")

class MatchingQuestion(BaseModel):
    question_type: str = Field(default="matching_pairs", description="Always 'matching'")
    instruction: str = Field(
        description="Brief instruction like 'Match each term to its definition'"
    )
    pairs: List[MatchingPair] = Field(
        description="3-4 pairs to match. Right side will be shuffled in UI."
    )

class OrderingQuestion(BaseModel):
    question_type: str = Field(default="arrange_Sentence", description="Always 'ordering'")
    question_text: str = Field(
        description="Question asking to put items in correct order"
    )
    correct_order: List[str] = Field(
        description="3-4 items in the CORRECT order (will be shuffled in UI)"
    )

# Union type for any question
Question = Union[MCQQuestion, FillInBlankQuestion, TrueFalseQuestion,
                 MatchingQuestion, OrderingQuestion]

class BiteSizedContent(BaseModel):
    pre_read: str = Field(
        description="Engaging 2-3 paragraph introduction (200-300 words). "
        "Conversational tone, use 'you', include relatable examples."
    )

    questions: List[Union[MCQQuestion, FillInBlankQuestion, TrueFalseQuestion,
                          MatchingQuestion, OrderingQuestion]] = Field(
        description="3-5 questions of VARIED types. Mix it up for engagement!"
    )

    summary: str = Field(
        description="Reinforcing summary (150-200 words) with real-world application. "
        "Celebrate learning and encourage curiosity."
    )

    concept_name: str = Field(description="The concept being taught")
    topic: str = Field(description="The parent topic")
    concept_description: str = Field(description="The concept being taught")
    key_takeaways: List[str] = Field(description="3-4 key points to remember")
    estimated_time: int = Field(description="Time in minutes (5-15)")
    difficulty_level: str = Field(description="beginner, intermediate, or advanced")
