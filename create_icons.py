#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
创建简单的 PNG 图标文件
需要安装 Pillow: pip install Pillow
"""

try:
    from PIL import Image, ImageDraw
    import os
    
    def create_icon(filename, color, size=(24, 24)):
        """创建简单的图标"""
        img = Image.new('RGBA', size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # 根据文件名绘制不同的图标
        if 'home' in filename:
            # 绘制房子图标
            points = [(12, 4), (20, 12), (18, 12), (18, 20), (6, 20), (6, 12), (4, 12)]
            draw.polygon(points, fill=color)
            draw.rectangle([10, 14, 14, 20], fill=color)
        elif 'category' in filename:
            # 绘制列表图标
            draw.rectangle([4, 6, 6, 8], fill=color)
            draw.rectangle([8, 6, 20, 8], fill=color)
            draw.rectangle([4, 10, 6, 12], fill=color)
            draw.rectangle([8, 10, 20, 12], fill=color)
            draw.rectangle([4, 14, 6, 16], fill=color)
            draw.rectangle([8, 14, 20, 16], fill=color)
        elif 'history' in filename:
            # 绘制时钟图标
            draw.ellipse([4, 4, 20, 20], outline=color, width=2)
            draw.line([12, 8, 12, 12], fill=color, width=2)
            draw.line([12, 12, 16, 14], fill=color, width=2)
        elif 'profile' in filename:
            # 绘制用户图标
            draw.ellipse([8, 6, 16, 14], outline=color, width=2)
            draw.arc([6, 14, 18, 22], 0, 180, fill=color, width=2)
        
        return img
    
    def main():
        """主函数"""
        # 确保 images 目录存在
        os.makedirs('images', exist_ok=True)
        
        # 定义颜色
        normal_color = (122, 126, 131)  # #7A7E83
        active_color = (74, 144, 226)   # #4A90E2
        
        # 创建图标
        icons = [
            ('images/home.png', normal_color),
            ('images/home-active.png', active_color),
            ('images/category.png', normal_color),
            ('images/category-active.png', active_color),
            ('images/history.png', normal_color),
            ('images/history-active.png', active_color),
            ('images/profile.png', normal_color),
            ('images/profile-active.png', active_color),
        ]
        
        for filename, color in icons:
            img = create_icon(filename, color)
            img.save(filename)
            print(f"创建图标: {filename}")
        
        print("所有图标创建完成！")
    
    if __name__ == "__main__":
        main()

except ImportError:
    print("需要安装 Pillow 库: pip install Pillow")
    print("或者您可以手动创建 24x24 像素的 PNG 图标文件")
    print("需要的文件:")
    print("- images/home.png")
    print("- images/home-active.png") 
    print("- images/category.png")
    print("- images/category-active.png")
    print("- images/history.png")
    print("- images/history-active.png")
    print("- images/profile.png")
    print("- images/profile-active.png")