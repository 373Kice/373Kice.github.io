#!/usr/bin/env ruby
# 更新Jekyll项目所有依赖的脚本

require 'fileutils'

puts "=== Jekyll项目依赖更新工具 ==="
puts "当前目录: #{Dir.pwd}"
puts

# 检查Gemfile是否存在
unless File.exist?("Gemfile")
  puts "❌ 错误: 当前目录没有Gemfile文件"
  exit 1
end

# 备份现有的Gemfile.lock
if File.exist?("Gemfile.lock")
  backup_file = "Gemfile.lock.backup-#{Time.now.strftime('%Y%m%d%H%M%S')}"
  FileUtils.cp("Gemfile.lock", backup_file)
  puts "✅ 已备份Gemfile.lock到: #{backup_file}"
end

# 1. 更新Bundler到最新版本
puts "\n1. 更新Bundler到最新版本..."
begin
  # 先检查当前bundler版本
  current_bundler = `bundle --version`.chomp rescue "未知"
  puts "   当前Bundler版本: #{current_bundler}"
  
  # 更新bundler
  puts "   正在更新Bundler..."
  system("gem update bundler")
  
  # 检查更新后的版本
  updated_bundler = `bundle --version`.chomp rescue "未知"
  puts "   更新后Bundler版本: #{updated_bundler}"
rescue => e
  puts "   ⚠️ 更新Bundler时出错: #{e.message}"
end

# 2. 检查Gemfile中的版本限制
puts "\n2. 分析Gemfile中的版本限制..."
gemfile_content = File.read("Gemfile")

# 找出所有gem定义
gem_patterns = gemfile_content.scan(/^\s*gem\s+["']([^"']+)["'](?:,\s*["']([^"']+)["'])?/)
if gem_patterns.any?
  puts "   发现 #{gem_patterns.length} 个gem定义:"
  gem_patterns.each_with_index do |(gem_name, version_constraint), i|
    puts "   #{i+1}. #{gem_name} #{version_constraint || '无版本限制'}"
  end
else
  puts "   未发现gem定义，请检查Gemfile格式"
end

# 3. 更新所有gem到最新版本
puts "\n3. 更新所有gem到最新版本..."
puts "   执行: bundle update --all"
system("bundle update --all")

if $?.success?
  puts "   ✅ 成功更新所有gem依赖"
else
  puts "   ❌ 更新失败，请检查错误信息"
end

# 4. 检查更新结果
puts "\n4. 检查更新结果..."
if File.exist?("Gemfile.lock")
  puts "   读取更新后的Gemfile.lock..."
  
  # 提取关键信息
  lock_content = File.read("Gemfile.lock")
  
  # 查找BUNDLED WITH行
  if lock_content.include?("BUNDLED WITH")
    bundled_with = lock_content.match(/BUNDLED WITH\s+(.+)/)
    puts "   BUNDLED WITH: #{bundled_with[1].strip}" if bundled_with
  end
  
  # 显示一些关键gem的版本
  key_gems = %w[jekyll jekyll-paginate kramdown rouge webrick sassc]
  key_gems.each do |gem_name|
    if lock_content.include?(gem_name)
      # 简单提取版本信息
      gem_line = lock_content.lines.find { |line| line.include?(gem_name) && line.include?("(") }
      puts "   #{gem_name}: #{gem_line.strip}" if gem_line
    end
  end
end

# 5. 清理和验证
puts "\n5. 验证依赖..."
puts "   执行: bundle check"
system("bundle check")

if $?.success?
  puts "   ✅ 依赖验证通过"
else
  puts "   ❌ 依赖验证失败"
  puts "   尝试修复: bundle install"
  system("bundle install")
end

puts "\n=== 更新完成 ==="
puts "建议步骤:"
puts "1. 运行 'bundle exec jekyll serve' 测试网站"
puts "2. 检查控制台是否有任何警告或错误"
puts "3. 验证网站所有功能是否正常工作"
puts "4. 如果遇到问题，可以使用备份文件恢复: #{backup_file}" if backup_file

puts "\n如果需要进一步更新Jekyll版本，可以:"
puts "1. 编辑Gemfile，将 'gem \"jekyll\", \"~> 4.2\"' 改为 'gem \"jekyll\"'"
puts "2. 运行 'bundle update jekyll'"
puts "3. 注意: Jekyll 5.x可能有破坏性变更，请谨慎更新"

puts "\n脚本完成。祝你网站运行顺利！ 🚀"