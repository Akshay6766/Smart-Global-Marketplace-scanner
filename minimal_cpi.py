# Read web_app.py
with open('web_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find where we add results to results_data and add CPI score
# Look for the section where hit_dict is created
old_section = '''        # Convert results to JSON-serializable format
        # Convert results with custom attributes
        results_data = []
        for hit in results:
            hit_dict = asdict(hit)
            if hasattr(hit, 'best_choice_reason'):
                hit_dict['best_choice_reason'] = hit.best_choice_reason
            if hasattr(hit, 'is_best_value'):
                hit_dict['is_best_value'] = hit.is_best_value
            
            results_data.append(hit_dict)'''

new_section = '''        # Convert results to JSON-serializable format
        # Convert results with custom attributes
        results_data = []
        for hit in results:
            hit_dict = asdict(hit)
            if hasattr(hit, 'best_choice_reason'):
                hit_dict['best_choice_reason'] = hit.best_choice_reason
            if hasattr(hit, 'is_best_value'):
                hit_dict['is_best_value'] = hit.is_best_value
            
            # Add CPI score (Spec Score from brand mapping)
            cpi_score = get_cpi_score(hit.title)
            hit_dict['cpi_score'] = cpi_score if cpi_score > 0 else 65
            
            results_data.append(hit_dict)'''

content = content.replace(old_section, new_section)

# Write back
with open('web_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Added CPI score to web_app.py results')
