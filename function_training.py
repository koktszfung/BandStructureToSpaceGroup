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


def validate_one_epoch(device, model, criterion, validate_loader):
    model.eval()
    num_validate = len(validate_loader.sampler.indices)
    if num_validate == 0:
        print("number of data is 0")
        return -1, -1
    val_loss = 0.
    num_correct = 0
    for b, (batch_input, batch_label) in enumerate(validate_loader):
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
        print("\r\tvalidate batch:{}/{}".format(b, len(validate_loader)), end="")
    val_loss /= num_validate
    num_correct /= num_validate
    return round(val_loss, 4), round(num_correct*100, 4)


def validate_train_loop(device, model, optimizer, scheduler, criterion, validate_loader, train_loader,
                        num_epoch, num_epoch_per_validate, state_dict_path):
    result = validate_one_epoch(device, model, criterion, validate_loader)
    print("\rvalidate loss:{} accuracy:{}%".format(*result))
    for epoch in range(num_epoch):
        result = train_one_epoch(device, model, optimizer, criterion, train_loader)
        print("\rtrain epoch:{} loss:{}".format(epoch, result))
        if (epoch + 1) % num_epoch_per_validate == 0:
            result = validate_one_epoch(device, model, criterion, validate_loader)
            print("\rvalidate loss:{} accuracy:{}%".format(*result))
        scheduler.step()
    torch.save(model.state_dict, state_dict_path)
