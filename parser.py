#!/usr/bin/env python3
"""
Magic: The Gathering Ability Parser
Uses Lark grammar to parse MTG card abilities and text.
"""

from lark import Lark, Transformer, v_args
from lark.exceptions import ParseError
import os
import re

class MTGTransformer(Transformer):
    """
    Transformer to convert parse tree into structured data.
    Customize this class to extract the information you need.
    """
    
    @v_args(inline=True)
    def ability(self, *args):
        return {"type": "ability", "components": list(args)}
    
    @v_args(inline=True)
    def planeswalker_ability(self, cost, text):
        return {"type": "planeswalker_ability", "cost": cost, "text": text}
    
    @v_args(inline=True)
    def mana_cost(self, *symbols):
        return {"type": "mana_cost", "symbols": list(symbols)}
    
    @v_args(inline=True)
    def effect(self, *args):
        return {"type": "effect", "details": list(args)}
    
    @v_args(inline=True)
    def trigger(self, *args):
        return {"type": "trigger", "details": list(args)}
    
    @v_args(inline=True)
    def static_ability(self, *args):
        return {"type": "static_ability", "details": list(args)}
    
    @v_args(inline=True)
    def activated_ability(self, cost, effect):
        return {"type": "activated_ability", "cost": cost, "effect": effect}
    
    def target(self, args):
        return {"type": "target", "description": " ".join(str(arg) for arg in args)}
    
    def pt(self, args):
        return {"type": "power_toughness", "power": args[0], "toughness": args[1]}
    
    def keyword(self, args):
        return {"type": "keyword", "name": " ".join(str(arg) for arg in args)}

class MTGAbilityParser:
    """
    Main parser class for MTG abilities.
    """
    
    def __init__(self, grammar_file=None, grammar_text=None):
        """
        Initialize parser with grammar.
        
        Args:
            grammar_file (str): Path to grammar file
            grammar_text (str): Grammar text directly
        """
        self._loaded = False
        if grammar_file:
            with open(grammar_file, 'r') as f:
                grammar = f.read()
        elif grammar_text:
            grammar = grammar_text
        else:
            # Use the provided grammar
            grammar = self._get_default_grammar()
        
        self.parser = Lark(grammar, start='start', parser='earley')
        self.transformer = MTGTransformer()
    
    def _get_default_grammar(self):
        """Returns the MTG grammar as a string."""
        if not self._loaded:
            self._loaded = True
            with open(os.path.join(os.path.dirname(__file__), 'grammar.txt')) as f:
                self._grammar = f.read()
        return self._grammar
    
    def preprocess_text(self, text):
        """
        Preprocess MTG text to handle placeholders and special cases.
        
        Args:
            text (str): Raw MTG ability text
            
        Returns:
            str: Preprocessed text ready for parsing
        """
        # Convert common symbols and terms
        preprocessed = text.replace("{T}", "TAP")
        
        # Handle placeholder tokens - you'll need to customize these based on your needs
        placeholder_map = {
            'COLOR_QUAL': ['white', 'blue', 'black', 'red', 'green', 'colorless'],
            'CARD_TYPE': ['creature', 'artifact', 'enchantment', 'instant', 'sorcery', 'land', 'planeswalker'],
            'SUB_TYPE': ['human', 'wizard', 'beast', 'soldier', 'equipment', 'aura'],
            'SUPER_TYPE': ['legendary', 'basic', 'snow'],
            'KEYWORD': ['flying', 'trample', 'vigilance', 'deathtouch', 'lifelink'],
            'COUNTER_TYPE': ['+1/+1 counter', 'loyalty counter', 'charge counter'],
            'STEP_OR_PHASE': ['upkeep', 'draw step', 'main phase', 'combat'],
            'QUANTITY': ['one', 'two', 'three', 'four', 'five'],
            'DIGIT': ['1', '2', '3', '4', '5'],
            'NUMBER_MOD': ['or more', 'or less', 'or fewer'],
            'ABILITY_IMPLICIT': ['flying', 'trample', 'haste'],
            'ABILITY': ['sacrifice', 'tap', 'discard', 'pay', 'exile']
        }
        
        # You might want to implement smarter placeholder replacement here
        # For now, we'll leave the text as-is for manual token replacement
        
        return preprocessed
    
    def parse(self, text, transform=True):
        """
        Parse MTG ability text.
        
        Args:
            text (str): MTG ability text to parse
            transform (bool): Whether to apply transformer
            
        Returns:
            Parse tree or transformed result
        """
        try:
            # Preprocess the text
            processed_text = self.preprocess_text(text)
            
            # Parse the text
            tree = self.parser.parse(processed_text)
            
            if transform:
                return self.transformer.transform(tree)
            else:
                return tree
                
        except ParseError as e:
            print(f"Parse error: {e}")
            return None
    
    def parse_multiple(self, texts, transform=True):
        """
        Parse multiple ability texts.
        
        Args:
            texts (list): List of MTG ability texts
            transform (bool): Whether to apply transformer
            
        Returns:
            List of parse results
        """
        results = []
        for text in texts:
            result = self.parse(text, transform)
            results.append(result)
        return results

def main():
    """
    Example usage of the MTG parser.
    """
    # Initialize parser
    parser = MTGAbilityParser()
    
    # Example ability texts (you'll need to replace placeholders with actual values)
    example_abilities = [
        # "TAP: draw a card",
        # "flying",
        # "when ~ enter the battlefield, draw a card",
        # "2, TAP: deal 1 damage to any target"
        "MANA, TAP: ABILITY a PT COLOR_QUAL SUB_TYPE CARD_TYPE token with KEYWORD named wood"
    ]
    
    print("MTG Ability Parser Example")
    print("=" * 40)
    
    for i, ability in enumerate(example_abilities, 1):
        print(f"\nExample {i}: '{ability}'")
        try:
            # Parse without transformation to see raw tree
            tree = parser.parse(ability, transform=False)
            if tree:
                print("Parse tree:", tree.pretty())
            
            # Parse with transformation
            result = parser.parse(ability, transform=True)
            if result:
                print("Transformed:", result)
            else:
                print("Failed to parse")
                
        except Exception as e:
            print(f"Error: {e}")
    
    print("\nNote: This grammar uses placeholder tokens (CARD_TYPE, COLOR_QUAL, etc.)")
    print("You'll need to replace these with actual values or implement")
    print("a more sophisticated preprocessing step.")

if __name__ == "__main__":
    main()
