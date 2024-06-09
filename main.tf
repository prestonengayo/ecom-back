provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "ecom" {
  name     = "ecom-resources"
  location = "West Europe"
}

resource "azurerm_virtual_network" "ecom" {
  name                = "ecom-network"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.ecom.location
  resource_group_name = azurerm_resource_group.ecom.name
}

resource "azurerm_subnet" "ecom" {
  name                 = "ecom-subnet"
  resource_group_name  = azurerm_resource_group.ecom.name
  virtual_network_name = azurerm_virtual_network.ecom.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_network_security_group" "ecom" {
  name                = "ecom-nsg"
  location            = azurerm_resource_group.ecom.location
  resource_group_name = azurerm_resource_group.ecom.name

  security_rule {
    name                       = "Allow_SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "Allow_API"
    priority                   = 1000
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "8000"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_public_ip" "ecom" {
  name                = "ecom-publicip"
  location            = azurerm_resource_group.ecom.location
  resource_group_name = azurerm_resource_group.ecom.name
  allocation_method   = "Static"
}

resource "azurerm_network_interface" "ecom" {
  name                = "ecom-nic"
  location            = azurerm_resource_group.ecom.location
  resource_group_name = azurerm_resource_group.ecom.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.ecom.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.ecom.id
  }
}

resource "azurerm_network_interface_security_group_association" "ecom" {
  network_interface_id      = azurerm_network_interface.ecom.id
  network_security_group_id = azurerm_network_security_group.ecom.id
}

resource "azurerm_linux_virtual_machine" "ecom" {
  name                = "ecom-vm"
  location            = azurerm_resource_group.ecom.location
  resource_group_name = azurerm_resource_group.ecom.name
  network_interface_ids = [azurerm_network_interface.ecom.id]

  size                 = "Standard_DS1_v2"
  admin_username       = "adminuser"
  disable_password_authentication = true

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  admin_ssh_key {
    username   = "adminuser"
    public_key = file("C:/Users/prest/.ssh/id_rsa.pub")
  }
}

resource "null_resource" "provision_vm" {
  depends_on = [azurerm_linux_virtual_machine.ecom]

  provisioner "file" {
    source      = "script.sh"
    destination = "/home/adminuser/script.sh"

    connection {
      type        = "ssh"
      user        = "adminuser"
      private_key = file("C:/Users/prest/.ssh/id_rsa")
      host        = azurerm_public_ip.ecom.ip_address
      timeout     = "2m"
    }
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /home/adminuser/script.sh",
      "sudo bash /home/adminuser/script.sh"
    ]

    connection {
      type        = "ssh"
      user        = "adminuser"
      private_key = file("C:/Users/prest/.ssh/id_rsa")
      host        = azurerm_public_ip.ecom.ip_address
      timeout     = "2m"
    }
  }
}

output "public_ip" {
  value = azurerm_public_ip.ecom.ip_address
}
