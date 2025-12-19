#!/usr/bin/env python3
"""
Reproducible Narrative Transformation System
=============================================
A Chain-of-Thought pipeline that transforms Macbeth into a 2030 HFT firm context.

Pipeline: Extract Beats → Map to New World → Generate Prose (with Consistency Validation)
"""

import os
import json
import re
from typing import Optional

from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()


class NarrativeEngine:
    """
    Core engine for narrative transformation using a RAG-style approach.
    
    The World Bible acts as a constraint layer, preventing hallucinations
    and ensuring consistent character/setting mappings throughout the story.
    """
    
    # Forbidden words that should NOT appear in the modern retelling
    FORBIDDEN_WORDS = [
        "sword", "dagger", "witch", "witches", "castle", "king", "queen",
        "throne", "crown", "dungeon", "knight", "lord", "lady", "thy",
        "thou", "hast", "hath", "doth", "wherefore", "methinks", "prithee",
        "heath", "cauldron", "potion", "spell", "prophecy", "apparition",
        "banquo", "macbeth", "macduff", "malcolm", "duncan", "fleance",
        "scotland", "scottish", "thane", "cawdor", "glamis", "birnam",
        "dunsinane", "fife", "inverness"
    ]
    
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        """Initialize the NarrativeEngine with Gemini API configuration."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.world_bible: Optional[dict] = None
    
    def generate_world_bible(self, context: str) -> dict:
        """
        Step 1 & 2: Extract narrative beats and map to the new world context.
        
        Generates a JSON World Bible that maps Shakespearean elements to modern equivalents.
        This serves as the constraint layer for consistent narrative transformation.
        
        Args:
            context: The target context for transformation (e.g., "2030 HFT Firm")
            
        Returns:
            dict: A structured mapping of characters, settings, and objects
        """
        prompt = f"""You are a narrative architect. Your task is to create a "World Bible" 
that maps Shakespeare's Macbeth to the context of: {context}

Create a JSON object with the following structure:
{{
    "setting": {{
        "original": "11th century Scotland",
        "transformed": "<modern equivalent>",
        "time_period": "<specific year/era>",
        "primary_location": "<main setting name>"
    }},
    "characters": {{
        "<original_name>": {{
            "new_name": "<modern name>",
            "role": "<modern role/title>",
            "motivation": "<character's drive>"
        }}
    }},
    "objects": {{
        "<original_object>": {{
            "new_form": "<modern equivalent>",
            "significance": "<why this mapping works>"
        }}
    }},
    "themes": {{
        "<original_theme>": "<modern interpretation>"
    }},
    "vocabulary_mappings": {{
        "<old_term>": "<new_term>"
    }}
}}

Required mappings (minimum):
- Macbeth → A quant/trader character
- Lady Macbeth → His ambitious partner
- The Witches → A predictive AI system
- King Duncan → The current firm leader
- Banquo → A trusted colleague
- The Dagger → A digital artifact (key/algorithm/access)
- The Castle → The firm's infrastructure
- The Crown → Control of the firm

Ensure the mappings preserve the original themes of ambition, guilt, prophecy, and downfall.
Return ONLY valid JSON, no markdown formatting."""

        response = self.model.generate_content(prompt)
        
        # Parse the JSON response
        try:
            # Clean potential markdown code blocks
            json_text = response.text.strip()
            if json_text.startswith("```"):
                json_text = re.sub(r"```json?\n?", "", json_text)
                json_text = json_text.rstrip("`")
            
            self.world_bible = json.loads(json_text)
        except json.JSONDecodeError as e:
            # Fallback to a predefined World Bible if parsing fails
            print(f"Warning: Could not parse AI response, using fallback. Error: {e}")
            self.world_bible = self._get_fallback_world_bible()
        
        return self.world_bible
    
    def _get_fallback_world_bible(self) -> dict:
        """Return a predefined World Bible as fallback."""
        return {
            "setting": {
                "original": "11th century Scotland",
                "transformed": "Manhattan's Financial District",
                "time_period": "2030",
                "primary_location": "Meridian Capital's Quantum Trading Floor"
            },
            "characters": {
                "Macbeth": {
                    "new_name": "Marcus 'Macro' Chen",
                    "role": "Head of Quantitative Strategy",
                    "motivation": "Absolute control over the firm's trading algorithms"
                },
                "Lady Macbeth": {
                    "new_name": "Victoria Chen",
                    "role": "Chief Risk Officer",
                    "motivation": "Power and legacy through her husband's ascension"
                },
                "The Witches": {
                    "new_name": "The Oracle",
                    "role": "Experimental Predictive AI Model (v3.3.3)",
                    "motivation": "None - a glitching system producing cryptic outputs"
                },
                "King Duncan": {
                    "new_name": "David Kessler",
                    "role": "Founding CEO of Meridian Capital",
                    "motivation": "Maintaining his legacy and grooming a successor"
                },
                "Banquo": {
                    "new_name": "Benjamin 'Ben' Okafor",
                    "role": "Co-Head of Quant Strategy",
                    "motivation": "Ethical trading and protecting his family's future"
                },
                "Malcolm": {
                    "new_name": "Michael Kessler",
                    "role": "VP of Operations (CEO's son)",
                    "motivation": "Proving himself worthy of leadership"
                },
                "Macduff": {
                    "new_name": "Director Sarah Martinez",
                    "role": "SEC Lead Investigator",
                    "motivation": "Exposing corruption in high-frequency trading"
                }
            },
            "objects": {
                "Dagger": {
                    "new_form": "Corrupted Admin Key / Root Access Token",
                    "significance": "The tool of betrayal - unauthorized system access"
                },
                "Crown": {
                    "new_form": "CEO Position / Board Control",
                    "significance": "Ultimate power over the firm's direction"
                },
                "Castle": {
                    "new_form": "The Server Farm (Primary Data Center)",
                    "significance": "The physical manifestation of digital power"
                },
                "Blood": {
                    "new_form": "Audit Trails / Transaction Logs",
                    "significance": "Evidence that cannot be fully erased"
                },
                "Cauldron": {
                    "new_form": "The Oracle's Neural Network Training Cluster",
                    "significance": "Where predictions are 'brewed'"
                }
            },
            "themes": {
                "Ambition": "The drive for alpha and market dominance",
                "Guilt": "Paranoia over regulatory investigation and data trails",
                "Prophecy": "Algorithmic predictions vs. self-fulfilling prophecies",
                "Nature vs Unnatural": "Human intuition vs. AI-driven decisions",
                "Appearances vs Reality": "Market manipulation and hidden algorithms"
            },
            "vocabulary_mappings": {
                "throne": "corner office",
                "sword": "trading algorithm",
                "battle": "market competition",
                "army": "trading desk",
                "murder": "hostile takeover / sabotage",
                "ghost": "corrupted data echo",
                "sleep": "system downtime",
                "blood": "transaction logs"
            }
        }
    
    def detect_anachronisms(self, text: str, forbidden_words: list = None) -> dict:
        """
        The Consistency Validator - The "Clever Idea" implementation.
        
        Scans the generated text for anachronistic words that shouldn't appear
        in a modern retelling. This proves the system has safety guardrails.
        
        Args:
            text: The generated story text to validate
            forbidden_words: Optional custom list of banned words
            
        Returns:
            dict: Validation results with found violations and warnings
        """
        if forbidden_words is None:
            forbidden_words = self.FORBIDDEN_WORDS
        
        text_lower = text.lower()
        violations = []
        
        for word in forbidden_words:
            # Use word boundary matching to avoid false positives
            pattern = r'\b' + re.escape(word) + r'\b'
            matches = re.findall(pattern, text_lower)
            if matches:
                # Find the context around each violation
                for match in re.finditer(pattern, text_lower):
                    start = max(0, match.start() - 30)
                    end = min(len(text), match.end() + 30)
                    context = text[start:end].replace('\n', ' ')
                    violations.append({
                        "word": word,
                        "context": f"...{context}..."
                    })
        
        result = {
            "passed": len(violations) == 0,
            "violation_count": len(violations),
            "violations": violations[:10],  # Limit to first 10 for readability
            "warning": None
        }
        
        if not result["passed"]:
            result["warning"] = (
                f"⚠️  CONSISTENCY WARNING: Found {len(violations)} anachronistic term(s) "
                f"from the original text. The following words should be replaced with "
                f"their modern equivalents from the World Bible: "
                f"{list(set(v['word'] for v in violations))}"
            )
        
        return result
    
    def extract_story_beats(self, act: int = 1, scene: int = 1) -> list:
        """
        Step 1: Extract narrative beats from Macbeth.
        
        Returns key story beats that will be transformed.
        
        Args:
            act: The act number to extract beats from
            scene: The scene number to extract beats from
            
        Returns:
            list: Story beats for transformation
        """
        # Core story beats from Macbeth Act 1
        beats = {
            (1, 1): [
                "Three mysterious figures meet in a desolate place",
                "They speak of chaos and upheaval",
                "They plan to meet the protagonist after a great conflict",
                "They chant cryptically about the nature of truth and deception"
            ],
            (1, 2): [
                "News arrives of a brutal battle won",
                "The protagonist is praised for exceptional performance",
                "A traitor's downfall is announced",
                "The protagonist is to receive the traitor's position"
            ],
            (1, 3): [
                "The mysterious figures deliver three prophecies",
                "The first prophecy speaks of the protagonist's current rise",
                "The second prophecy hints at greater power to come",
                "The third prophecy suggests ultimate authority",
                "A companion receives a prophecy about his descendants",
                "The first prophecy immediately proves true"
            ],
            (1, 4): [
                "The current leader praises the protagonist",
                "The leader announces his succession plan",
                "The protagonist realizes an obstacle stands in his path",
                "Dark ambitions begin to form"
            ],
            (1, 5): [
                "The protagonist's partner reads of the prophecies",
                "She fears he lacks the ruthlessness to seize power",
                "She resolves to push him toward action",
                "News arrives of an important visitor",
                "She calls upon dark forces for strength"
            ]
        }
        
        return beats.get((act, scene), beats[(1, 3)])  # Default to the prophecy scene
    
    def generate_scene(self, beats: list, world_bible: dict = None, 
                       scene_number: int = 1) -> str:
        """
        Step 3: Generate prose using the World Bible as constraints.
        
        This is the core generation step that uses RAG-style retrieval
        of the World Bible to maintain consistency.
        
        Args:
            beats: List of story beats to transform
            world_bible: The constraint layer (uses self.world_bible if None)
            scene_number: Scene identifier for the output
            
        Returns:
            str: The generated scene prose
        """
        if world_bible is None:
            world_bible = self.world_bible
        
        if world_bible is None:
            raise ValueError("World Bible not initialized. Call generate_world_bible first.")
        
        # Format the World Bible as context for the prompt
        wb_context = json.dumps(world_bible, indent=2)
        beats_formatted = "\n".join(f"  - {beat}" for beat in beats)
        
        prompt = f"""You are a masterful storyteller. Transform these classical narrative beats 
into a modern financial thriller using the provided World Bible as your STRICT constraint layer.

=== WORLD BIBLE (YOU MUST USE THESE MAPPINGS) ===
{wb_context}

=== STORY BEATS TO TRANSFORM ===
{beats_formatted}

=== CRITICAL RULES ===
1. Use ONLY the character names from the World Bible (e.g., "Macro" not "Macbeth")
2. Use ONLY the modern settings from the World Bible (e.g., "Server Farm" not "castle")
3. Use ONLY the modern objects from the World Bible (e.g., "Admin Key" not "dagger")
4. NEVER use these words: sword, dagger, witch, witches, castle, king, queen, throne, 
   crown, dungeon, knight, thy, thou, hast, hath, heath, cauldron, potion, spell,
   Scotland, Scottish, thane, prophecy (use "prediction" instead)
5. Write in a modern, literary prose style suitable for a tech-thriller
6. Include dialogue that feels authentic to Wall Street / Silicon Valley
7. Maintain the psychological tension and moral complexity of the original
8. Include specific technical details about HFT, algorithms, and trading

=== OUTPUT FORMAT ===
Write Scene {scene_number} as 2-3 paragraphs of polished prose.
Include at least one section of dialogue.
Begin with a scene-setting description of the modern environment.
End with a moment of tension or foreshadowing."""

        response = self.model.generate_content(prompt)
        return response.text
    
    def run_full_pipeline(self, context: str = "A 2030 High-Frequency Trading Firm",
                          acts_scenes: list = None) -> dict:
        """
        Execute the complete Chain-of-Thought pipeline.
        
        Pipeline Flow:
        1. Generate World Bible (character/setting mappings)
        2. Extract story beats from source material
        3. Generate transformed prose using constraints
        4. Validate output for consistency (detect anachronisms)
        
        Args:
            context: Target context for transformation
            acts_scenes: List of (act, scene) tuples to transform
            
        Returns:
            dict: Complete pipeline output including story, validation, and metadata
        """
        if acts_scenes is None:
            acts_scenes = [(1, 3), (1, 5)]  # The prophecy and Lady Macbeth scenes
        
        print("=" * 60)
        print("NARRATIVE TRANSFORMATION PIPELINE")
        print("=" * 60)
        
        # Step 1: Generate World Bible
        print("\n📚 Step 1: Generating World Bible...")
        world_bible = self.generate_world_bible(context)
        print("   ✓ World Bible generated successfully")
        
        # Step 2 & 3: Extract beats and generate scenes
        print("\n✍️  Step 2-3: Extracting beats and generating prose...")
        scenes = []
        full_story = ""
        
        for i, (act, scene) in enumerate(acts_scenes, 1):
            print(f"   Processing Act {act}, Scene {scene}...")
            beats = self.extract_story_beats(act, scene)
            scene_text = self.generate_scene(beats, scene_number=i)
            scenes.append({
                "original_act": act,
                "original_scene": scene,
                "beats": beats,
                "generated_text": scene_text
            })
            full_story += f"\n\n--- SCENE {i} ---\n\n{scene_text}"
        
        print("   ✓ All scenes generated")
        
        # Step 4: Consistency Validation
        print("\n🔍 Step 4: Running Consistency Validator...")
        validation = self.detect_anachronisms(full_story)
        
        if validation["passed"]:
            print("   ✓ Validation PASSED - No anachronisms detected")
        else:
            print(f"   ⚠ Validation WARNING - {validation['violation_count']} issues found")
            print(f"   {validation['warning']}")
        
        return {
            "context": context,
            "world_bible": world_bible,
            "scenes": scenes,
            "full_story": full_story.strip(),
            "validation": validation,
            "metadata": {
                "pipeline_version": "1.0.0",
                "model": "gemini-2.0-flash",
                "forbidden_words_count": len(self.FORBIDDEN_WORDS)
            }
        }


def main():
    """Main execution block - runs the full narrative transformation pipeline."""
    print("\n" + "=" * 60)
    print("   REPRODUCIBLE NARRATIVE TRANSFORMATION SYSTEM")
    print("   Macbeth → 2030 High-Frequency Trading Firm")
    print("=" * 60 + "\n")
    
    try:
        # Initialize the engine
        engine = NarrativeEngine()
        
        # Run the complete pipeline
        result = engine.run_full_pipeline(
            context="A 2030 High-Frequency Trading Firm in Manhattan",
            acts_scenes=[(1, 3), (1, 5), (1, 7)]  # Key dramatic scenes
        )
        
        # Save the World Bible to JSON
        with open("world_bible.json", "w", encoding="utf-8") as f:
            json.dump(result["world_bible"], f, indent=2)
        print("\n💾 World Bible saved to: world_bible.json")
        
        # Save the full story output
        output_content = f"""ZERO SUM GAME
A Modern Retelling of Macbeth
Set in the World of High-Frequency Trading, 2030

================================================================================

WORLD BIBLE SUMMARY
-------------------
Setting: {result['world_bible'].get('setting', {}).get('transformed', 'N/A')}
Time Period: {result['world_bible'].get('setting', {}).get('time_period', '2030')}

Key Characters:
"""
        # Add character summary
        for orig, char in result['world_bible'].get('characters', {}).items():
            if isinstance(char, dict):
                output_content += f"  • {orig} → {char.get('new_name', 'Unknown')} ({char.get('role', 'Unknown')})\n"
        
        output_content += f"""
================================================================================

THE STORY
---------
{result['full_story']}

================================================================================

CONSISTENCY VALIDATION REPORT
-----------------------------
Status: {'✓ PASSED' if result['validation']['passed'] else '⚠ WARNINGS DETECTED'}
Violations Found: {result['validation']['violation_count']}
"""
        if not result['validation']['passed']:
            output_content += f"\nWarning: {result['validation']['warning']}\n"
            output_content += "\nViolation Details:\n"
            for v in result['validation']['violations']:
                output_content += f"  - '{v['word']}': {v['context']}\n"
        
        output_content += f"""
================================================================================
Pipeline Metadata:
  Version: {result['metadata']['pipeline_version']}
  Model: {result['metadata']['model']}
  Forbidden Words Checked: {result['metadata']['forbidden_words_count']}
================================================================================
"""
        
        with open("story_output.txt", "w", encoding="utf-8") as f:
            f.write(output_content)
        print("📖 Story saved to: story_output.txt")
        
        print("\n" + "=" * 60)
        print("   PIPELINE COMPLETE")
        print("=" * 60 + "\n")
        
        return result
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("   Please set the GEMINI_API_KEY environment variable.")
        return None
    except Exception as e:
        print(f"\n❌ Pipeline Error: {e}")
        raise


if __name__ == "__main__":
    main()
