//
//  ContentView.swift
//  Demo01
//
//  Created by lm on 2026/7/10.
//

import SwiftUI

struct AppItem: Identifiable, Hashable {
    let id = UUID()
    let title: String
    let iconName: String
    let color: Color
}

struct ContentView: View {
    private let apps: [AppItem] = [
        AppItem(title: "Safari", iconName: "safari", color: .blue),
        AppItem(title: "邮件", iconName: "mail", color: .blue),
        AppItem(title: "信息", iconName: "message", color: .green),
        AppItem(title: "日历", iconName: "calendar", color: .red),
        AppItem(title: "照片", iconName: "photo", color: .purple),
        AppItem(title: "音乐", iconName: "music", color: .orange),
        AppItem(title: "视频", iconName: "film", color: .blue),
        AppItem(title: "备忘录", iconName: "note", color: .yellow),
        AppItem(title: "提醒事项", iconName: "alarm", color: .orange),
        AppItem(title: "地图", iconName: "map", color: .green),
        AppItem(title: "天气", iconName: "cloud", color: .cyan),
        AppItem(title: "时钟", iconName: "clock", color: .black),
        AppItem(title: "计算器", iconName: "calculator", color: .gray),
        AppItem(title: "App Store", iconName: "bag", color: .blue),
        AppItem(title: "设置", iconName: "gear", color: .gray),
        AppItem(title: "照片", iconName: "camera", color: .gray),
        AppItem(title: "播客", iconName: "mic", color: .purple),
        AppItem(title: "股市", iconName: "trending.up", color: .green),
        AppItem(title: "图书", iconName: "book", color: .orange),
        AppItem(title: "快捷指令", iconName: "wand.and.stars", color: .purple),
        AppItem(title: "FaceTime", iconName: "video", color: .green),
        AppItem(title: "电话", iconName: "phone", color: .green),
        AppItem(title: "通讯录", iconName: "person", color: .blue),
        AppItem(title: "文件", iconName: "folder", color: .yellow),
    ]
    
    var body: some View {
        NavigationStack {
            ScrollView {
                LazyVGrid(columns: [GridItem(.adaptive(minimum: 80))], spacing: 20) {
                    ForEach(apps) { app in
                        NavigationLink(value: app) {
                            VStack(spacing: 8) {
                                ZStack {
                                    RoundedRectangle(cornerRadius: 16)
                                        .fill(app.color.opacity(0.15))
                                        .frame(width: 64, height: 64)
                                    Image(systemName: app.iconName)
                                        .resizable()
                                        .aspectRatio(contentMode: .fit)
                                        .frame(width: 32, height: 32)
                                        .foregroundColor(app.color)
                                }
                                Text(app.title)
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                                    .multilineTextAlignment(.center)
                            }
                        }
                    }
                }
                .padding()
            }
            .navigationTitle("启动台")
            .navigationDestination(for: AppItem.self) { app in
                DetailView(app: app)
            }
        }
    }
}

struct DetailView: View {
    let app: AppItem
    
    var body: some View {
        VStack(spacing: 30) {
            ZStack {
                RoundedRectangle(cornerRadius: 24)
                    .fill(app.color.opacity(0.2))
                    .frame(width: 120, height: 120)
                Image(systemName: app.iconName)
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(width: 60, height: 60)
                    .foregroundColor(app.color)
            }
            
            Text(app.title)
                .font(.title)
                .fontWeight(.bold)
            
            Text("这是 \(app.title) 的详情页面")
                .foregroundColor(.secondary)
            
            Spacer()
        }
        .padding()
        .navigationTitle(app.title)
    }
}

#Preview {
    ContentView()
}
