#!/usr/bin/python3
"""Command interpreter for AfriBnB"""
import cmd
import sys
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class AFRIBNBCommand(cmd.Cmd):
    """Command interpreter class"""

    prompt = "(afribnb) "
    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True
    
    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def emptyline(self):
        """Do nothing on empty input line"""
        pass
    
    def do_create(self, arg):
        """Create a new instance of a class"""
        if not arg:
            print("** class name missing **")
            return
        if arg not in self.classes:
            print("** class doesn't exist **")
            return
        new_instance = self.classes[arg]()
        new_instance.save()
        print(new_instance.id)
    
    def do_show(self, arg):
        """Show string representation of an instance"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[key])
    
    def do_destroy(self, arg):
        """Delete an instance"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()
    
    def do_all(self, arg):
        """Print all instances"""
        obj_list = []
        if not arg:
            for obj in storage.all().values():
                obj_list.append(str(obj))
        elif arg in self.classes:
            for key, obj in storage.all().items():
                if key.split(".")[0] == arg:
                    obj_list.append(str(obj))
        else:
            print("** class doesn't exist **")
            return
        print(obj_list)
    
    def do_update(self, arg):
        """Update an instance attribute"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        
        obj = storage.all()[key]
        attr_name = args[2]
        attr_value = args[3].strip('"')

        # Try to cast appropriate type
        if attr_value.isdigit():
            attr_value = int(attr_value)
        elif attr_value.replace('.', '', 1).isdigit():
            attr_value = float(attr_value)
        
        setattr(obj, attr_name, attr_value)
        obj.save()

if __name__ == "__main__":
    AFRIBNBCommand().cmdloop()