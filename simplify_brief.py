#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re

def simplify_brief(brief, name):
    """精简brief到20字以内，尽量保留关键信息"""
    if not brief or not isinstance(brief, str):
        return brief
    
    # 移除多余的空格
    brief = re.sub(r'\s+', ' ', brief).strip()
    
    # 如果已经是20字以内，直接返回
    if len(brief) <= 20:
        return brief
    
    # 尝试按分号、句号分割，取前两部分组合
    parts = re.split(r'[；;。]', brief)
    parts = [p.strip() for p in parts if p.strip()]
    
    if parts:
        # 尝试组合前两部分
        if len(parts) >= 2:
            combined = parts[0] + '，' + parts[1]
            if len(combined) <= 20:
                return combined
        
        # 如果第一部分在20字以内，使用第一部分
        if len(parts[0]) <= 20:
            return parts[0]
        
        # 如果第一部分太长，尝试按逗号分割
        comma_parts = re.split(r'[，,]', parts[0])
        comma_parts = [p.strip() for p in comma_parts if p.strip()]
        
        if comma_parts:
            # 尝试组合前两个逗号部分
            if len(comma_parts) >= 2:
                combined = comma_parts[0] + '，' + comma_parts[1]
                if len(combined) <= 20:
                    return combined
            
            # 使用第一个逗号部分
            if len(comma_parts[0]) <= 20:
                return comma_parts[0]
    
    # 如果都不行，直接截取前20字
    brief = brief[:20]
    
    # 如果截取后最后一个字符是标点，移除
    if brief and brief[-1] in '，。；、':
        brief = brief[:-1]
    
    return brief.strip()

def enhance_brief(brief, name):
    """增强过短的brief，使其更完整但仍保持在20字以内"""
    if not brief or len(brief) >= 20:
        return brief
    
    # 如果brief太短（少于10字），尝试添加一些描述
    if len(brief) < 10:
        additions = []
        
        # 根据菜品名称和现有brief，生成更完整的描述
        if '包' in name or '包子' in name or '饺' in name:
            if '面皮' not in brief and '松软' not in brief:
                additions.append('面皮松软')
            if '馅料' not in brief and '鲜美' not in brief:
                additions.append('馅料鲜美')
        elif '汤' in name or '羹' in name:
            if '汤' not in brief and '鲜美' not in brief:
                additions.append('汤汁鲜美')
            if '营养' not in brief:
                additions.append('营养丰富')
        elif '炒' in name or '爆' in name:
            if '色香' not in brief and '味' not in brief and '俱全' not in brief:
                additions.append('色香味俱全')
        elif '炸' in name or '烤' in name or '煎' in name:
            if '外酥' not in brief and '里嫩' not in brief:
                additions.append('外酥里嫩')
            elif '香气' not in brief:
                additions.append('香气四溢')
        elif '蒸' in name:
            if '鲜嫩' not in brief and '滑爽' not in brief:
                additions.append('鲜嫩滑爽')
            elif '原汁' not in brief:
                additions.append('原汁原味')
        elif '炖' in name or '煮' in name or '煲' in name:
            if '软烂' not in brief and '入味' not in brief:
                additions.append('软烂入味')
            elif '营养' not in brief:
                additions.append('营养丰富')
        elif '拌' in name or '凉' in name:
            if '清爽' not in brief and '开胃' not in brief:
                additions.append('清爽开胃')
        elif '烧' in name or '焖' in name or '红烧' in name:
            if '酱香' not in brief and '浓郁' not in brief:
                additions.append('酱香浓郁')
        
        # 如果没有添加任何内容，且brief中没有"美味"相关词汇，添加一个
        if not additions and '美味' not in brief and '可口' not in brief and '好吃' not in brief:
            additions.append('美味可口')
        
        # 组合添加的内容
        if additions:
            enhanced = brief
            for addition in additions:
                test = enhanced + '，' + addition
                if len(test) <= 20:
                    enhanced = test
                else:
                    break
            
            return enhanced
    
    return brief

def process_recipe_data(input_file, output_file):
    """处理RecipeData.json，精简brief字段"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"总记录数: {len(data)}")
        
        updated_count = 0
        examples = []
        for i, item in enumerate(data):
            original_brief = item.get('brief', '')
            name = item.get('name', '')
            current_brief = original_brief
            
            # 先精简过长的brief
            if original_brief and len(original_brief) > 20:
                current_brief = simplify_brief(original_brief, name)
                item['brief'] = current_brief
                updated_count += 1
                if len(examples) < 10:
                    examples.append({
                        'name': name,
                        'original': original_brief,
                        'simplified': current_brief,
                        'type': '精简'
                    })
            
            # 再增强过短的brief
            if current_brief and len(current_brief) < 10:
                enhanced = enhance_brief(current_brief, name)
                if enhanced != current_brief and len(enhanced) <= 20:
                    item['brief'] = enhanced
                    if len(examples) < 15:
                        examples.append({
                            'name': name,
                            'original': current_brief,
                            'simplified': enhanced,
                            'type': '增强'
                        })
        
        print(f"\n共处理 {updated_count} 条记录的brief字段\n")
        if examples:
            print("示例更新结果:")
            for ex in examples[:15]:
                print(f"\n{ex['name']} ({ex['type']}):")
                print(f"  原: {ex['original']} ({len(ex['original'])}字)")
                print(f"  新: {ex['simplified']} ({len(ex['simplified'])}字)")
        
        # 验证所有brief都在20字以内
        long_briefs = [(i+1, item['name'], item['brief'], len(item['brief'])) 
                      for i, item in enumerate(data) 
                      if len(item.get('brief', '')) > 20]
        
        if long_briefs:
            print(f"\n警告: 仍有 {len(long_briefs)} 条记录超过20字:")
            for idx, name, brief, length in long_briefs[:5]:
                print(f"  {idx}. {name}: {brief} ({length}字)")
        else:
            print(f"\n✓ 所有记录的brief都在20字以内")
        
        # 保存到输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n已保存到: {output_file}")
        return True
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    input_file = 'RecipeData.json'
    output_file = 'RecipeData.json'
    
    print("开始处理RecipeData.json...")
    success = process_recipe_data(input_file, output_file)
    
    if success:
        print("\n处理完成！")
    else:
        print("\n处理失败！")
