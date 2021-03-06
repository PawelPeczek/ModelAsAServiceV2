import torchvision

if __name__ == '__main__':
    print("Model weights fetching...")
    _ = torchvision.models.detection.retinanet_resnet50_fpn(pretrained=True)
    print("Done.")
