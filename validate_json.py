#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys

def validate_recipe_data(file_path):
    """验证RecipeData.json的数据格式"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print("错误: 根元素应该是数组")
            return False
        
        print(f"总记录数: {len(data)}")
        
        required_fields = ['id', 'name', 'imageSrc', 'brief', 'categoryIds', 'difficulty', 'time']
        optional_fields = ['ingredients', 'steps']
        
        issues = []
        
        for i, item in enumerate(data):
            # 检查必需字段
            for field in required_fields:
                if field not in item:
                    issues.append(f"记录 {i+1}: 缺少必需字段 '{field}'")
                elif item[field] is None:
                    issues.append(f"记录 {i+1}: 字段 '{field}' 为 null")
            
            # 检查字段类型
            if 'id' in item and not isinstance(item['id'], str):
                issues.append(f"记录 {i+1}: 'id' 应该是字符串")
            
            if 'name' in item and not isinstance(item['name'], str):
                issues.append(f"记录 {i+1}: 'name' 应该是字符串")
            
            if 'imageSrc' in item and not isinstance(item['imageSrc'], str):
                issues.append(f"记录 {i+1}: 'imageSrc' 应该是字符串")
            
            if 'brief' in item and not isinstance(item['brief'], str):
                issues.append(f"记录 {i+1}: 'brief' 应该是字符串")
            
            if 'categoryIds' in item:
                if not isinstance(item['categoryIds'], list):
                    issues.append(f"记录 {i+1}: 'categoryIds' 应该是数组")
                else:
                    for j, cat_id in enumerate(item['categoryIds']):
                        if not isinstance(cat_id, str):
                            issues.append(f"记录 {i+1}: 'categoryIds[{j}]' 应该是字符串")
            
            if 'difficulty' in item and not isinstance(item['difficulty'], str):
                issues.append(f"记录 {i+1}: 'difficulty' 应该是字符串")
            
            if 'time' in item and not isinstance(item['time'], str):
                issues.append(f"记录 {i+1}: 'time' 应该是字符串")
            
            if 'ingredients' in item and item['ingredients'] is not None:
                if not isinstance(item['ingredients'], str):
                    issues.append(f"记录 {i+1}: 'ingredients' 应该是字符串")
            
            if 'steps' in item and item['steps'] is not None:
                if not isinstance(item['steps'], list):
                    issues.append(f"记录 {i+1}: 'steps' 应该是数组")
                else:
                    for j, step in enumerate(item['steps']):
                        if not isinstance(step, str):
                            issues.append(f"记录 {i+1}: 'steps[{j}]' 应该是字符串")
        
        if issues:
            print(f"\n发现问题: {len(issues)} 个")
            for issue in issues[:20]:  # 只显示前20个问题
                print(f"  - {issue}")
            if len(issues) > 20:
                print(f"  ... 还有 {len(issues) - 20} 个问题")
            return False
        else:
            print("所有记录格式都合法")
            return True
            
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return False
    except Exception as e:
        print(f"错误: {e}")
        return False

if __name__ == '__main__':
    file_path = 'RecipeData.json'
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    
    success = validate_recipe_data(file_path)
    sys.exit(0 if success else 1)

