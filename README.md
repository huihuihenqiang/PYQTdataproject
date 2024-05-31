## README

### 项目概述

🚀 **基础数据处理框架** 是一个基于 PyQt 的多功能数据处理框架，专为数据导入、预处理和可视化设计。此框架为 **钻井漏失数据处理软件 v1.0.1** 提供了基础结构[document](https://huihuihenqiang.github.io/article/Software/help.html)，展示了高效的多线程处理、状态栏实时更新等高级技术功能。

![图片](https://github.com/huihuihenqiang/PYQTdataproject/assets/99072450/56bfd759-d7cb-48c3-aaa4-2ac32a4e0555)


### 功能特点

- **状态栏**：实时显示软件运行状态、提示信息及辅助信息。🛠️
- **多线程支持**：提高数据处理效率，支持同时处理多个文件。⚡
- **数据导入**：支持Excel和PDF文件的导入。📥
- **数据预处理**：自动清洗、筛选和转换数据。🧹
- **数据可视化**：提供多种图表类型，如折线图和散点图。📊
- **工作区域管理**：支持多任务并行处理，允许创建和管理多个独立的工作区域。📂

### 技术细节

- **PyQt**：用于创建用户界面，使得界面直观友好。
- **多线程处理**：通过Python的`threading`模块，实现数据处理的并行化，显著提高了处理速度。
- **数据可视化**：使用`matplotlib`库生成多种类型的图表，帮助用户直观地分析数据。
- **数据处理**：利用`pandas`库进行数据清洗、转换和合并，使得数据处理更加高效便捷。
- **状态栏集成**：实时显示当前操作状态和进度，提供良好的用户体验。

### 安装与运行

1. 克隆仓库
    ```bash
    git clone https://github.com/huihuihenqiang/PYQTdataproject.git
    ```

2. 安装依赖
    ```bash
    pip install -r requirements.txt
    ```

3. 运行项目
    ```bash
    python main.py
    ```

### 贡献

欢迎贡献代码！请提交Pull Request，我们会尽快审核。

---

## README

### Project Overview

🚀 **Basic Data Processing Framework** is a versatile data processing framework based on PyQt, designed for data import, preprocessing, and visualization. This framework serves as the foundational structure for the **Drilling Loss Data Processing Software v1.0.1** [document](https://huihuihenqiang.github.io/article/Software/help.html), showcasing advanced technical features such as efficient multithreading processing and real-time status bar updates.

![图片](https://github.com/huihuihenqiang/PYQTdataproject/assets/99072450/135d1e2f-884e-41d9-b85f-1793c7aaa09f)

### Features

- **Status Bar**: Displays real-time software running status, prompt messages, and auxiliary information. 🛠️
- **Multithreading Support**: Improves data processing efficiency, supporting simultaneous processing of multiple files. ⚡
- **Data Import**: Supports importing Excel and PDF files. 📥
- **Data Preprocessing**: Automatically cleans, filters, and transforms data. 🧹
- **Data Visualization**: Provides various chart types, such as line charts and scatter plots. 📊
- **Workspace Management**: Supports multitasking parallel processing, allowing the creation and management of multiple independent workspaces. 📂

### Technical Details

- **PyQt**: Used for creating the user interface, making it intuitive and user-friendly.
- **Multithreading**: Implemented using Python's `threading` module to parallelize data processing, significantly improving processing speed.
- **Data Visualization**: Utilized the `matplotlib` library to generate various types of charts, aiding users in intuitive data analysis.
- **Data Processing**: Employed the `pandas` library for data cleaning, transformation, and merging, making data handling more efficient and convenient.
- **Status Bar Integration**: Displays current operation status and progress in real-time, providing an excellent user experience.

### Installation and Running

1. Clone the repository
    ```bash
    git clone https://github.com/huihuihenqiang/PYQTdataproject.git
    ```

2. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

3. Run the project
    ```bash
    python main.py
    ```

### Contributing

We welcome contributions! Please submit a Pull Request, and we will review it as soon as possible.
