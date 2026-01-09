from typing import List, Dict, Any, Set

class KnowledgeTransferCore:
    """
    Pure logic for Knowledge Transfer.
    Handles merging of lesson datasets.
    """

    def merge_lessons(self, current_lessons: List[Any], imported_lessons: List[Any]) -> List[Any]:
        """Merges imported lessons into the current set, avoiding duplicates."""
        # Normalize to dicts only
        valid_current = [l for l in current_lessons if isinstance(l, dict)]
        valid_imported = [l for l in imported_lessons if isinstance(l, dict)]
        
        # Create a signature set for existing lessons
        # Signature = (failure_context, correction) usually unique enough
        seen_signatures: Set[str] = set()
        
        for l in valid_current:
            sig = f"{l.get('failure_context')}|{l.get('correction')}"
            seen_signatures.add(sig)
            
        merged = list(valid_current) # Start with current
        
        for lesson in valid_imported:
            sig = f"{lesson.get('failure_context')}|{lesson.get('correction')}"
            if sig not in seen_signatures:
                merged.append(lesson)
                seen_signatures.add(sig)
                
        return merged
