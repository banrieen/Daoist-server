import wx

class ImagePreview(wx.Frame):
    def __init__(self, parent, title, image_paths):
        super(ImagePreview, self).__init__(parent, title=title, size=(600, 400))
        
        self.image_paths = image_paths
        self.current_index = 0
        self.all_images_previewed = False
        
        # 创建面板
        panel = wx.Panel(self)
        
        # 创建图像控件
        self.image_ctrl = wx.StaticBitmap(panel, -1)
        self.update_image()
        
        # 创建左侧按钮
        self.left_button = wx.Button(panel, label='<')
        self.left_button.Bind(wx.EVT_BUTTON, self.on_left_button)
        
        # 创建右侧按钮
        self.right_button = wx.Button(panel, label='>')
        self.right_button.Bind(wx.EVT_BUTTON, self.on_right_button)
        
        # 创建布局
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.left_button, 0, wx.ALL | wx.CENTER, 5)
        hbox.Add(self.image_ctrl, 1, wx.EXPAND | wx.CENTER, 5)
        hbox.Add(self.right_button, 0, wx.ALL | wx.CENTER, 5)
        
        panel.SetSizer(hbox)
        
        # 最大化窗口
        self.Maximize()
        
        # 将窗口置顶
        self.Raise()
        
        # 设置窗口居中
        self.Centre()
        self.Show()

    def update_image(self):
        image = wx.Image(self.image_paths[self.current_index], wx.BITMAP_TYPE_ANY)
        self.image_ctrl.SetBitmap(wx.Bitmap(image))
        self.Refresh()

    def on_left_button(self, event):
        if not self.all_images_previewed:
            self.current_index = (self.current_index - 1) % len(self.image_paths)
            self.update_image()

    def on_right_button(self, event):
        if not self.all_images_previewed:
            self.current_index = (self.current_index + 1) % len(self.image_paths)
            self.update_image()
            if self.current_index == len(self.image_paths) - 1:
                self.all_images_previewed = True

    def OnClose(self, event):
        if self.all_images_previewed:
            self.Destroy()
        else:
            event.Veto()

if __name__ == '__main__':
    app = wx.App()
    image_paths = [r"../target_image/ST1HN-10/1_F(90, 1) #1-34.jpg" , r"../target_image/ST1HN-10/2_F(91, 2) #1-40.jpg" , r'../target_image/ST1HN-10/4_F(94, 5) #1-12.jpg']
    ImagePreview(None, 'Image Preview', image_paths)
    app.MainLoop()
