#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

def check_briefs(file_path):
    """检查brief字段"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"总记录数: {len(data)}")
    
    long_briefs = []
    duplicates = []
    
    for i, item in enumerate(data):
        brief = item.get('brief', '')
        name = item.get('name', '')
        length = len(brief)
        
        if length > 20:
            long_briefs.append((i+1, name, brief, length))
        
        # 检查是否有重复的部分
        if '，' in brief:
            parts = brief.split('，')
            if len(parts) >= 2:
                # 检查是否有完全相同的部分
                for j in range(len(parts)-1):
                    if parts[j].strip() == parts[j+1].strip():
                        duplicates.append((i+1, name, brief))
                        break
    
    print(f"\n超过20字的记录: {len(long_briefs)}")
    if long_briefs:
        for idx, name, brief, length in long_briefs[:5]:
            print(f"  {idx}. {name}: {brief} ({length}字)")
    
    print(f"\n可能有重复的记录: {len(duplicates)}")
    if duplicates:
        for idx, name, brief in duplicates[:5]:
            print(f"  {idx}. {name}: {brief}")
    
    # 显示前10条记录
    print("\n前10条记录的brief:")
    for i, item in enumerate(data[:10]):
        brief = item.get('brief', '')
        name = item.get('name', '')
        print(f"{i+1}. {name}: {brief} ({len(brief)}字)")

if __name__ == '__main__':
    check_briefs('RecipeData.json')

