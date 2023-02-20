Java.perform(function() {
    // hook Ljava/io/File;
    var classFile = Java.use("java.io.File");
    if(classFile) {
        var doListLog = false
        // hook constructor
        classFile.$init.overload("java.lang.String").implementation = function(path) {
            var retval = this.$init.overload("java.lang.String").apply(this, arguments);
            if(path.indexOf("font") == -1) {
                console.log(this.class + "@" + this.hashCode(), 
                "| Ljava/io/File; | <init> | (Ljava/lang/String;)V | " + path + " | ");
                doListLog = true
            }
            return retval;
        }
        
        // hook Ljava/io/File;->list
        classFile.list.overloads[0].implementation = function() {
            var retval = this.list.overloads[0].apply(this, arguments);
            if(doListLog)
                console.log(this.class + "@" +  this.hashCode(), "| Ljava/io/File; | list | ()[Ljava/lang/String; | | " + retval);
            return retval;
        }

        classFile.list.overloads[0].implementation = function() {
            var retval = this.list.overloads[0].apply(this, arguments);
            if(doListLog)
                console.log(this.class + "@" +  this.hashCode(), 
                "| Ljava/io/File; | list | (Ljava/io/FilenameFilter;)[Ljava/lang/String; | | " + retval);
            return retval;
        }

        // hook Ljava/io/File;->listFiles
        classFile.listFiles.overloads[0].implementation = function() {
            var retval = this.listFiles.overloads[0].apply(this, arguments);
            if(doListLog)
                console.log(this.class + "@" +  this.hashCode(), 
                "| Ljava/io/File; | listFiles | ()[Ljava/io/File; | | " + retval);
            return retval;
        }

        classFile.listFiles.overloads[1].implementation = function() {
            var retval = this.listFiles.overloads[1].apply(this, arguments);
            if(doListLog)
                console.log(this.class + "@" +  this.hashCode(), 
                "| Ljava/io/File; | listFiles | (Ljava/io/FilenameFilter;)[Ljava/io/File; | | " + retval);
            return retval;
        }
        
        classFile.listFiles.overloads[2].implementation = function() {
            var retval = this.listFiles.overloads[2].apply(this, arguments);
            if(doListLog)
                console.log(this.class + "@" +  this.hashCode(), 
                "| Ljava/io/File; | listFiles | (Ljava/io/FileFilter;)[Ljava/io/File; | | @" + retval);
            return retval;
        }
    }

    // hook java.lang.Runtime
    var classRuntime = Java.use("java.lang.Runtime");
    if(classRuntime) {
        // hook getRuntime
        // static method
        classRuntime.getRuntime.implementation = function() {
            var retval = this.getRuntime.apply(this, arguments);
            console.log(this.class, "| Ljava/lang/Runtime; | getRuntime | ()Ljava/lang/Runtime; | | @" + retval.hashCode());
            return retval;
        }

        // hook exec
        classRuntime.exec.overloads[0].implementation = function(command) {
            var retval = this.exec.overloads[0].apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(), 
            "| Ljava/lang/Runtime; | exec | (Ljava/lang/String;)Ljava/lang/Process; | " + command + " | @" + retval.hashCode());
            return retval;
        }

        classRuntime.exec.overloads[1].implementation = function(command, _) {
            var retval = this.exec.overloads[1].apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(), 
            "| Ljava/lang/Runtime; | exec | Ljava/lang/String; [Ljava/lang/String;)Ljava/lang/Process; | " + command + " | @" + retval.hashCode());
            return retval;
        }

        classRuntime.exec.overloads[2].implementation = function(command, _, __) {
            var retval = this.exec.overloads[2].apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(), 
            "| Ljava/lang/Runtime; | exec | (Ljava/lang/String; [Ljava/lang/String; Ljava/io/File;)Ljava/lang/Process; | " + command + " | @" + retval.hashCode());
            return retval;
        }

        classRuntime.exec.overloads[3].implementation = function(command) {
            var retval = this.exec.overloads[3].apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(), 
            "| Ljava/lang/Runtime; | exec | (Ljava/lang/String;)Ljava/lang/Process; | " + command + " | @" + retval.hashCode());
            return retval;
        }

        classRuntime.exec.overloads[4].implementation = function(command, _) {
            var retval = this.exec.overloads[4].apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(), 
            "| Ljava/lang/Runtime; | exec | (Ljava/lang/String; [Ljava/lang/String;)Ljava/lang/Process; | " + command + " | @" + retval.hashCode());
            return retval;
        }

        classRuntime.exec.overloads[5].implementation = function(command, _, __) {
            var retval = this.exec.overloads[5].apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(), 
            "| Ljava/lang/Runtime; | exec | (Ljava/lang/String; [Ljava/lang/String; Ljava/io/File;)Ljava/lang/Process; | " + command + " | @" + retval.hashCode());
            return retval;
        }
    }

    // hook java.lang.ProcessBuilder
    var classProcessBuilder = Java.use("java.lang.ProcessBuilder");
    if(classProcessBuilder) {
        // hook constructor
        classProcessBuilder.$init.overload("java.util.List").implementation = function(arg) {
            var retval = this.$init.overload("java.util.List").apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(), 
            "| Ljava/lang/ProcessBuilder; | <init> | (Ljava.util.List;)V | " + arg + " | ");
            return retval;
        }

        classProcessBuilder.$init.overload("[Ljava.lang.String;").implementation = function(str) {
            var retval = this.$init.overload("[Ljava.lang.String;").apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(), 
            "| Ljava/lang/ProcessBuilder; | <init> | ([Ljava.lang.String;)V | " + str + " | ");
            return retval;
        }

        // hook start
        classProcessBuilder.start.overload().implementation = function() {
            var retval = this.start.overload().apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(), 
            "| Ljava/lang/ProcessBuilder; | start | ()Ljava/lang/Process; | | @" + retval.hashCode());
            return retval;
        }
    }

    var classIntent = Java.use("android.content.Intent");
    if(classIntent) {
        classIntent.$init.overload("java.lang.String").implementation = function(action) {
            var retval = this.$init.overload("java.lang.String").apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(), 
            "| Landroid/content/Intent; | <init> | (Ljava/lang/String;)V | " + action + " | ");
            return retval;
        }

        for(let i = 0 ; i < 25 ; i++) {
            classIntent.putExtra.overloads[i].implementation = function(name, _) {
                var retval = this.putExtra.apply(this, arguments);
                console.log(this.class + "@" +  this.hashCode(), 
                "| Landroid/content/Intent; | putExtra | (Ljava/lang/String; DontCare)Landroid/content/Intent; | " + name + " | @" + retval.hashCode());
                return retval;
            }
        }
    }

    // hook Activity
    var classActivity = Java.use("android.app.Activity");
    if(classActivity) {
        // hook startActivityForResult
        classActivity.startActivityForResult.overload("android.content.Intent", "int", "android.os.Bundle").implementation = function(intent, _, __) {
            var retval = this.startActivityForResult.overload("android.content.Intent", "int", "android.os.Bundle").apply(this, arguments);
            console.log(this.class + "@" + this.hashCode(), 
            "| Landroid/app/Activity; | startActivityForResult | (Landroid/content/Intent; I Landroid/os/Bundle;)V | " + 
            intent.class + "@" + intent.hashCode() + " | ");
            return retval;
        };

        // hook getSystemService    
        classActivity.getSystemService.overload("java.lang.String").implementation = function(str) {
            var retval = this.getSystemService.overload("java.lang.String").apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(), 
            "| Landroid/app/Activity; | getSystemService | (Ljava/lang/String;)Ljava/lang/Object | " + str + " | @" + retval.hashCode());
            return retval;
        }
    }

    // have to check
    var classUsageStatsManager = Java.use("android.app.usage.UsageStatsManager");
    if(classUsageStatsManager) {
        classUsageStatsManager.queryEvents.overload("long", "long").implementation = function(_, __) {
            var retval = this.queryEvents.overload("long", "long").apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(), 
            "| Landroid/app/usage/UsageStatsManager; | queryEvents | (J J)Landroid/app/usage/UsageEvents; | | @" + retval.hashCode());
            return retval;
        }
    }

    var classUsageEvents_Event = Java.use("android.app.usage.UsageEvents$Event");
    if(classUsageEvents_Event) {
        classUsageEvents_Event.$init.overload().implementation = function() {
            var retval = this.$init.overload().apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(), 
            "| Landroid/app/usage/UsageEvents$Event; | <init> | ()V | | ");
            return retval;
        }
    }

    var classContext = Java.use("android.content.ContextWrapper");
    if(classContext) {
        classContext.getContentResolver.implementation = function() {
            var retval = this.getContentResolver.apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(),
            "| Landroid/content/ContextWrapper; | getContentResolver | ()Landroid/content/ContentResolver; | | @" + retval.hashCode());
            return retval;
        }
    }

    var classContentResolver = Java.use("android.content.ContentResolver");
    if(classContentResolver) {
        classContentResolver.query.overload('android.net.Uri', '[Ljava.lang.String;', 
        'android.os.Bundle', 'android.os.CancellationSignal').implementation = function(uri, _, __, ___, ____) {
            var retval = this.query.overload('android.net.Uri', '[Ljava.lang.String;', 
            'android.os.Bundle', 'android.os.CancellationSignal').apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(),
            "| Landroid/content/ContentResolver; | query | (Landroid/net/Uri; [Ljava/lang/String; Landroid/os/Bundle; Landroid/os/CancellationSignal;)Landroid/database/Cursor; | "
             + uri + " | " + Java.cast(retval, Java.use("android.content.ContentResolver$CursorWrapperInner")).hashCode());
            
            return retval;
        }
    }

    var classCursorWrapper = Java.use("android.database.CursorWrapper");
    if(classCursorWrapper) {
        classCursorWrapper.getColumnIndexOrThrow.implementation = function(column) {
            var retval = this.getColumnIndexOrThrow.apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(),
            "| Landroid/database/CursorWrapper; | getColumnIndexOrThrow | (Ljava/lang/String;)I  | " + column + " | " + retval);
            return retval;
        }

        classCursorWrapper.getColumnIndex.implementation = function(column) {
            var retval = this.getColumnIndex.apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(),
            "| Landroid/database/CursorWrapper; | getColumnIndex | (Ljava/lang/String;)I | " + column + " | " + retval);
            return retval;
        }

        classCursorWrapper.getString.implementation = function(index) {
            var retval = this.getString.apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(),
            "| Landroid/database/CursorWrapper; | getString | (I)Ljava/lang/String; | " + index + " | " + retval);
            return retval;
        }
    }

    var classLocationManager = Java.use("android.location.LocationManager");
    if(classLocationManager) {
        classLocationManager.isProviderEnabled.implementation = function(str) {
            var retval = this.getString.apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(),
            "| Landroid/location/LocationManager; | isProviderEnabled | (Ljava/lang/String)Z | " + str + " | " + retval);
            return retval;
        }

        classLocationManager.getLastKnownLocation.overload("java.lang.String", "android.location.LastLocationRequest").implementation = function(str, _) {
            var retval = this.getString.apply(this, arguments);
            console.log(this.class + "@" +  this.hashCode(),
            "| Landroid/location/LocationManager; | getLastKnownLocation | (Ljava/lang/String; Landroid/location/LocationRequest;)Landroid/location/Location; | " + str + " | " + retval);
            return retval;
        }
    }

    var classLocation = Java.use("android.location.Location");
    if(classLocation) {
        classLocation.$init.overload("java.lang.String").implementation = function(str) {
            var retval = this.$init.overload("java.lang.String").apply(this, arguments);
            console.log(this.class + "@" + this.hashCode(), 
            "| Landroid/location/Location; | <init> | (Ljava/lang/String;)V  | " + str + " | " + retval);
            return retval;
        }

        classLocation.$init.overload("android.location.Location").implementation = function(location) {
            var retval = this.$init.overload("android.location.Location").apply(this, arguments);
            console.log(this.class + "@" + this.hashCode(), 
            "| Landroid/location/Location; | <init> | (Landroid/location/Location;)V  | " + location + " | ");
            return retval;
        }

        classLocation.getTime.implementation = function() {
            var retval = this.getTime.apply(this, arguments);
            console.log(this.class + "@" + this.hashCode(), 
            "| Landroid/location/Location; | getTime | ()J  | | " + retval);
            return retval;
        }

        classLocation.getLatitude.implementation = function() {
            var retval = this.getLatitude.apply(this, arguments);
            console.log(this.class + "@" + this.hashCode(), 
            "| Landroid/location/Location; | getTime | ()J  | | " + retval);
            return retval;
        }

        classLocation.getLongtitude.implementation = function() {
            var retval = this.getLongtitude.apply(this, arguments);
            console.log(this.class + "@" + this.hashCode(), 
            "| Landroid/location/Location; | getTime | ()J  | | " + retval);
            return retval;
        }

        classLocation.toString.implementation = function() {
            var retval = this.toString.apply(this, arguments);
            console.log(this.class + "@" + this.hashCode(), 
            "| Landroid/location/Location; | toString | ()Ljava/lang/String;  | | " + retval);
            return retval;
        }
    }
});