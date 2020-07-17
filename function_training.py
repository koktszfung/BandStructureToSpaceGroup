import torch


def train_one_epoch(device, model, optimizer, criterion, train_loader):
    model.train()
    loss_epoch = 0.
    for b, (batch_input, batch_label) in enumerate(train_loader):
        for i in range(len(batch_input)):
            # reset gradient history
            optimizer.zero_grad()
            # read data
            data_input, data_label = batch_input[i], batch_label[i]
            data_input, data_label = data_input.to(device), data_label.to(device)
            # feed
            output = model(data_input).view(1, -1)
            loss = criterion(output, data_label)
            loss.backward()
            optimizer.step()
            loss_epoch = loss.item()
        print("\r\ttrain batch:{}/{}".format(b, len(train_loader)), end="")
    return round(loss_epoch, 4)


def validate_one_epoch(device, model, criterion, valid_loader):
    model.eval()
    num_valid = len(valid_loader.sampler.indices)
    if num_valid == 0:
        raise FileNotFoundError("number of data is 0")
    val_loss = 0.
    num_correct = 0
    for b, (batch_input, batch_label) in enumerate(valid_loader):
        for i in range(len(batch_input)):
            # read data
            data_input, data_label = batch_input[i], batch_label[i]
            data_input, data_label = data_input.to(device), data_label.to(device)
            # feed
            output = model(data_input).view(1, -1)
            # record fitness
            val_loss += criterion(output, data_label).item()
            if torch.max(output, 1)[1] == data_label:
                num_correct += 1
        print("\r\tvalid batch:{}/{}".format(b, len(valid_loader)), end="")
    num_correct /= num_valid
    return round(val_loss, 4), round(num_correct*100, 4)


def validate_train_loop(device, model, optimizer, scheduler, criterion, valid_loader, train_loader,
                        num_epoch, num_epoch_per_valid, state_dict_path):
    result = validate_one_epoch(device, model, criterion, valid_loader)
    print("\rvalid loss:{} accuracy:{}%".format(*result))
    for epoch in range(num_epoch):
        result = train_one_epoch(device, model, optimizer, criterion, train_loader)
        print("\rtrain epoch:{} loss:{}".format(epoch, result))
        if (epoch + 1) % num_epoch_per_valid == 0:
            result = validate_one_epoch(device, model, criterion, valid_loader)
            print("\rvalid loss:{} accuracy:{}%".format(*result))
        scheduler.step()
    torch.save(model.state_dict(), state_dict_path)