.class public Lmx/hackdefender/ctf/consultavotantes/MainActivity;
.super Landroidx/appcompat/app/AppCompatActivity;
.source "MainActivity.java"


# instance fields
.field vote:Landroid/widget/Button;


# direct methods
.method public constructor <init>()V
    .locals 0

    .line 9
    invoke-direct {p0}, Landroidx/appcompat/app/AppCompatActivity;-><init>()V

    return-void
.end method

.method private getIP1()Ljava/lang/String;
    .locals 1

    const-string v0, "52"

    return-object v0
.end method

.method private getIP2()Ljava/lang/String;
    .locals 1

    .line 31
    invoke-direct {p0}, Lmx/hackdefender/ctf/consultavotantes/MainActivity;->interF2()I

    move-result v0 #### 0x5

    add-int/lit8 v0, v0, 0xa ### v0 15

    .line 32
    invoke-static {v0}, Ljava/lang/Integer;->toString(I)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method private getIP4()Ljava/lang/String;
    .locals 1

    .line 45
    invoke-virtual {p0}, Lmx/hackdefender/ctf/consultavotantes/MainActivity;->interF4()I

    move-result v0 #99

    rsub-int v0, v0, 0xc1

    .line 46                        # >>>>>>>> 94
    invoke-static {v0}, Ljava/lang/Integer;->toString(I)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method private interF2()I
    .locals 1

    const/4 v0, 0x5

    return v0
.end method

.method private interF3()I
    .locals 1

    const/16 v0, 0x10

    return v0
.end method


# virtual methods
.method public getIP3()Ljava/lang/String;
    .locals 2

    .line 38
    invoke-direct {p0}, Lmx/hackdefender/ctf/consultavotantes/MainActivity;->interF3()I

    move-result v0 #16

    const/16 v1, 0xe60

    div-int/2addr v1, v0

    .line 39
    invoke-static {v1}, Ljava/lang/Integer;->toString(I)Ljava/lang/String;

    move-result-object v0

    return-object v0 #230
.end method

.method public getPort()I
    .locals 3

    const/4 v0, 0x0

    const/4 v1, 0x0

    :goto_0
    const/16 v2, 0x3e8

    if-gt v0, v2, :cond_0

    add-int/lit16 v1, v1, 0x122 #290 1 teracion

    add-int/lit8 v0, v0, 0x64 # 100

    goto :goto_0

    :cond_0
    return v1
.end method # 7216

.method public interF4()I
    .locals 1

    const/16 v0, 0x63

    return v0
.end method

.method public makeConnectionFunc(Landroid/view/View;)V
    .locals 3

    .line 20
    new-instance p1, Ljava/lang/StringBuilder;

    invoke-direct {p1}, Ljava/lang/StringBuilder;-><init>()V

    invoke-direct {p0}, Lmx/hackdefender/ctf/consultavotantes/MainActivity;->getIP1()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {p1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v0, "."

    invoke-virtual {p1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-direct {p0}, Lmx/hackdefender/ctf/consultavotantes/MainActivity;->getIP2()Ljava/lang/String; ######>>>>>> 52.

    move-result-object v1 ##### >>>>>> 15 

    invoke-virtual {p1, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder; ### >>>>>52.15.

    invoke-virtual {p0}, Lmx/hackdefender/ctf/consultavotantes/MainActivity;->getIP3()Ljava/lang/String; ####

    move-result-object v1

    invoke-virtual {p1, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder; #230

    invoke-direct {p0}, Lmx/hackdefender/ctf/consultavotantes/MainActivity;->getIP4()Ljava/lang/String;

    move-result-object v0  

    invoke-virtual {p1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1   # >>>>>>>> 52.15.230.94

    .line 21
    sget-object v0, Ljava/lang/System;->out:Ljava/io/PrintStream;  # >>>>>>>> 52.15.230.94

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "IP address: " 

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1  # >>>>>>> "IP address: 52.15.230.94" 52.15.230.94:

    invoke-virtual {v0, p1}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    .line 22
    sget-object p1, Ljava/lang/System;->out:Ljava/io/PrintStream;

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "Port: "

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {p0}, Lmx/hackdefender/ctf/consultavotantes/MainActivity;->getPort()I

    move-result v1 

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0 "Port: 7216"

    invoke-virtual {p1, v0}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    return-void 
.end method             52.15.230.94:7213


.method protected onCreate(Landroid/os/Bundle;)V
    .locals 0

    .line 14
    invoke-super {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->onCreate(Landroid/os/Bundle;)V

    const p1, 0x7f09001c

    .line 15
    invoke-virtual {p0, p1}, Lmx/hackdefender/ctf/consultavotantes/MainActivity;->setContentView(I)V

    const p1, 0x7f070092

    .line 16
    invoke-virtual {p0, p1}, Lmx/hackdefender/ctf/consultavotantes/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object p1

    check-cast p1, Landroid/widget/Button;

    iput-object p1, p0, Lmx/hackdefender/ctf/consultavotantes/MainActivity;->vote:Landroid/widget/Button;

    return-void
.end method
