class PIIVault:

    def __init__(self):
        self.mask_map = {}
        self.unmask_map = {}
        self.counter = {}

    def generate_token(self, entity_type):

        if entity_type not in self.counter:
            self.counter[entity_type] = 1
        else:
            self.counter[entity_type] += 1
        
        return f"[{entity_type}_{self.counter[entity_type]}]"
    
    # Mask function
    def mask_text(self, text, analysis_results):
        masked_text = text

        for result in analysis_results:
            value = text[result.start:result.end]
            entity = result.entity_type

            if value not in self.mask_map:
                
                token = self.generate_token(entity)

                self.mask_map[value] = token
                self.unmask_map[token] = value

            masked_text = masked_text.replace(value, self.mask_map[value])
        
        return masked_text
    
    # Unmask function
    def unmask_text(self, text):

        unmasked_text = text

        for token, value in self.unmask_map.items():
            unmasked_text = unmasked_text.replace(token, value)

        return unmasked_text