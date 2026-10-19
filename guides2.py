"""More guides. Each: (slug, title, meta description, html body)."""
def more(lk):
    U, M, Z, D, F = lk('800016537860','Ubuntu'), lk('800016421272','Linux Mint'), lk('800034663198','Zorin OS'), lk('800016323704','Debian'), lk('800016354792','Fedora')
    return [
("how-to-try-linux-without-installing", "How to try Linux without installing it",
 "Run Linux from a USB drive in live mode and test it on your own computer without changing Windows or your files.",
 f"""<p>You do not have to commit to Linux to find out whether you like it. A live USB runs the whole system from the drive, leaving your computer's disk untouched.</p>
<h2>What you need</h2><ul><li>A bootable USB drive such as {U}, {M} or {Z}.</li><li>A computer that can <a href="guide-how-to-boot-from-usb.html">boot from USB</a>.</li><li>About 15 minutes.</li></ul>
<h2>Steps</h2><ol><li>Plug in the drive and restart.</li><li>Open the boot menu and choose the USB drive.</li><li>Select the option to try the system rather than install it.</li><li>Test Wi-Fi, sound, printing, your browser and the apps you rely on.</li><li>Shut down and remove the drive. Your computer starts as before.</li></ol>
<h2>What to expect</h2><p>Live mode is a little slower than an installed system because it reads from USB. A faster drive helps. Changes are usually not kept unless the drive has <a href="guide-what-is-persistence-on-a-live-usb.html">persistence</a>.</p>"""),
("how-to-create-a-bootable-usb-drive", "How to create a bootable USB drive",
 "How bootable USB drives are made, the tools people use, and when it is easier to start with a ready-made drive.",
 f"""<p>Making a bootable drive means writing an operating system image to a USB drive in a way a computer can start from. It is not the same as copying files across.</p>
<h2>The usual method</h2><ol><li>Download the system image (an ISO file) from the official website of the operating system.</li><li>Verify the checksum if the site provides one.</li><li>Use a writing tool such as Rufus on Windows, balenaEtcher on Windows, Mac and Linux, or <a href="guide-what-is-ventoy.html">Ventoy</a> to write the image.</li><li>Check that the drive starts the computer.</li></ol>
<h2>Common problems</h2><ul><li>Wrong partition scheme for your computer (GPT for UEFI, MBR for older BIOS).</li><li>Interrupted downloads that give a damaged image.</li><li>Cheap or failing drives that cause random errors.</li></ul>
<h2>The shortcut</h2><p>If you would rather skip the downloading and writing, a ready-made drive such as {U} or {M} arrives set up and ready to start.</p>"""),
("how-to-fix-a-usb-drive-that-will-not-boot", "USB drive not booting? Fixes that work",
 "Troubleshooting steps for a USB drive that does not appear in the boot menu or will not start a computer.",
 """<p>If your computer ignores the USB drive, the cause is almost always a setting rather than a fault. Work through these in order.</p>
<h2>Quick checks</h2><ul><li>Use a USB port directly on the computer, preferably at the back of a desktop.</li><li>Try USB 2.0 ports if USB 3 ports are not detected.</li><li>Press the boot menu key repeatedly right after power on. See the <a href="guide-boot-menu-keys-by-brand.html">boot menu keys</a>.</li></ul>
<h2>Firmware settings</h2><ul><li>Move USB up in the boot order.</li><li>Choose the UEFI entry for the drive when two are listed.</li><li>Check <a href="guide-secure-boot-and-linux.html">Secure Boot</a> if the system is blocked.</li><li>Switch storage mode from RAID to AHCI if your internal drive is missing from an installer.</li></ul>
<h2>Windows keeps starting</h2><p>Windows Fast Startup can skip the boot menu. Shut down fully by holding Shift while selecting Shut down, then try again.</p>
<h2>Still stuck?</h2><p>Message us through our eBay store with your computer model and we will help you work out the right settings. Read <a href="guide-uefi-vs-legacy-bios-boot.html">UEFI vs legacy BIOS</a> for background.</p>"""),
("how-to-back-up-before-installing-linux", "How to back up your files before installing Linux",
 "A simple backup checklist to complete before installing a new operating system or changing disk partitions.",
 """<p>Installing an operating system can change or erase partitions. A backup turns a possible disaster into a minor inconvenience.</p>
<h2>What to save</h2><ul><li>Documents, photos and videos.</li><li>Browser bookmarks and saved passwords export.</li><li>Email archives and app data you cannot download again.</li><li>Software licence keys.</li></ul>
<h2>Where to save it</h2><ul><li>An external hard drive or SSD.</li><li>Cloud storage you already use.</li><li>A second USB drive for small amounts of data.</li></ul>
<h2>Check the backup</h2><p>Open a few files from the backup drive to confirm they work. Keep the backup disconnected during installation so it cannot be selected by mistake.</p>
<p>Next step: <a href="guide-how-to-install-linux-from-usb.html">install Linux from USB</a>.</p>"""),
("how-to-check-your-pc-works-with-linux", "How to check your PC works with Linux",
 "Check hardware compatibility for Linux by testing a live USB: Wi-Fi, graphics, sound, touchpad and more.",
 f"""<p>Most computers work with Linux, but the best test is to try it. A live USB shows how your actual hardware behaves before you change anything.</p>
<h2>What to test</h2><ul><li>Wi-Fi and Bluetooth.</li><li>Screen resolution and brightness keys.</li><li>Sound through speakers and headphones.</li><li>Touchpad gestures, webcam and microphone.</li><li>Suspend and resume on a laptop.</li></ul>
<h2>Good first systems to test</h2><p>{U} and {M} include broad hardware support. {F} often brings newer drivers for recent hardware.</p>
<h2>If something does not work</h2><p>Search the model of the device with the word Linux, or try another distribution. Driver support differs between systems."""+"</p>"),
("linux-vs-windows-which-is-right-for-you", "Linux vs Windows: which is right for you?",
 "A fair comparison of Linux and Windows for everyday use, gaming, work and older computers.",
 f"""<p>Both systems do the everyday jobs well. The better fit depends on what you do and the software you depend on.</p>
<h2>Where Linux stands out</h2><ul><li>Runs well on older hardware.</li><li>No forced restarts for updates mid-task on most distributions.</li><li>Large library of software available from built-in app stores.</li><li>Highly customisable.</li></ul>
<h2>Where Windows stands out</h2><ul><li>Widest support for commercial software.</li><li>Many games and anti-cheat systems are Windows-first.</li><li>Hardware makers often ship Windows drivers first.</li></ul>
<h2>The middle path</h2><p>You can keep both with <a href="guide-how-to-dual-boot-linux-and-windows.html">dual booting</a>. For a gentle start, try {Z} or {M}, which feel familiar to Windows users.</p>"""),
("how-to-install-software-on-linux", "How to install software on Linux",
 "App stores, package managers, Flatpak and AppImage explained in plain language for new Linux users.",
 f"""<p>Installing software on Linux is usually easier than people expect. Most systems include an app store.</p>
<h2>Main ways</h2><ul><li><strong>Software centre:</strong> search, click Install. Best for beginners.</li><li><strong>Package manager:</strong> a command such as apt (Ubuntu, Mint, Debian) or dnf ({F}).</li><li><strong>Flatpak:</strong> a universal app format available on most distributions.</li><li><strong>AppImage:</strong> a single file you download, mark as executable and run.</li></ul>
<h2>Good habits</h2><ul><li>Prefer your system's own repositories.</li><li>Download from official project sites only.</li><li>Keep the system updated.</li></ul>
<p>Beginner-friendly systems with strong app stores include {U}, {M} and {Z}.</p>"""),
("best-linux-for-programming", "Best Linux for programming and developers",
 "Which Linux distributions suit developers, from stable Debian to up-to-date Fedora and Ubuntu.",
 f"""<p>Linux is a natural home for development: native command line, package managers and servers that run the same system.</p>
<h2>Popular choices</h2><ul><li>{U}: huge community and tutorials, widely used for cloud work.</li><li>{F}: newer tools and kernels, favoured by many developers.</li><li>{D}: rock-solid stability for long-running machines.</li><li>{M}: comfortable desktop based on Ubuntu.</li></ul>
<h2>What to look for</h2><ul><li>Easy installation of compilers, Docker and language runtimes.</li><li>An LTS release if you want fewer changes (see <a href="guide-lts-vs-regular-releases.html">LTS vs regular</a>).</li><li>Good hardware support for your laptop.</li></ul>"""),
("best-linux-for-privacy-and-security", "Best Linux for privacy and security",
 "Linux options for privacy-minded users, including security-focused systems and sensible habits.",
 f"""<p>Linux gives you control over what runs on your computer. Some systems go further.</p>
<h2>Security-focused systems</h2><ul><li>Qubes OS isolates activities into separate virtual machines. It suits experienced users and needs capable hardware.</li><li>{D} and {F} receive prompt security updates and are widely audited.</li></ul>
<h2>Habits that matter more than the distro</h2><ul><li>Apply updates promptly.</li><li>Use full disk encryption when installing.</li><li>Use strong, unique passwords and a password manager.</li><li>Install apps only from trusted sources.</li></ul>
<p>See also <a href="guide-is-linux-safe-to-use.html">is Linux safe to use</a>.</p>"""),
("how-to-update-linux", "How to keep Linux updated",
 "Simple steps to update Linux safely: updater tools, kernel updates, restarts and release upgrades.",
 """<p>Updates fix security problems and bugs. On Linux they are normally quick and do not force a restart.</p>
<h2>Everyday updates</h2><ul><li>Open the Software Updater or Update Manager and apply what is listed.</li><li>Restart when prompted, usually only after kernel updates.</li><li>Turn on automatic security updates if offered.</li></ul>
<h2>Moving to a new release</h2><ul><li>Back up first.</li><li>LTS releases offer upgrades between versions through the updater.</li><li>A fresh install from a new <a href="guide-how-to-boot-from-usb.html">bootable USB</a> is the cleanest route.</li></ul>"""),
("linux-on-a-mac", "Can you run Linux on a Mac?",
 "What works on Intel and Apple silicon Macs, and how to start Linux from a USB drive on a Mac.",
 """<p>Yes on many Macs, with an important difference between old and new models.</p>
<h2>Intel Macs</h2><p>Hold the Option key at start-up and choose the USB drive. Many distributions run well, though Wi-Fi and some hardware may need extra drivers.</p>
<h2>Apple silicon Macs</h2><p>Standard x86 USB installers do not start on these Macs. Dedicated projects target Apple silicon, and virtual machines are the easiest way to run Linux there.</p>
<h2>Tips</h2><ul><li>Test with a live USB first.</li><li>Back up with Time Machine.</li><li>Older Intel Macs make excellent Linux machines.</li></ul>"""),
("usb-3-vs-usb-2-for-live-linux", "USB 3 or USB 2: which is better for live Linux?",
 "How drive speed affects live Linux, installation time and persistence, and what to look for in a USB drive.",
 """<p>Speed matters most when you run Linux directly from the drive.</p>
<h2>The difference</h2><ul><li>USB 3 drives load the system and apps noticeably faster.</li><li>USB 2 works, but boots and opens programs more slowly.</li><li>Plugging a USB 3 drive into a USB 2 port limits it to USB 2 speed.</li></ul>
<h2>Which to choose</h2><ul><li>Occasional rescue or install use: either is fine.</li><li>Daily live use with persistence: choose USB 3 or a fast SD card.</li></ul>
<p>Read about <a href="guide-live-usb-or-install.html">live USB vs installing</a> to decide how you will use it.</p>"""),
("what-is-a-linux-distribution", "What is a Linux distribution?",
 "Plain-English explanation of Linux distributions, desktops and why there are so many to choose from.",
 f"""<p>Linux is the core of the system (the kernel). A distribution, or distro, bundles that kernel with a desktop, apps and an installer into something you can use.</p>
<h2>Why so many?</h2><p>Different groups build for different goals: simplicity, stability, speed, gaming, security or tiny hardware. You pick the one that matches your needs.</p>
<h2>Families</h2><ul><li>Debian family: {D}, {U}, {M}, {Z}.</li><li>Red Hat family: {F}.</li><li>Independent systems such as Arch and Gentoo.</li></ul>
<h2>Desktop environments</h2><p>The look and feel comes from the desktop: GNOME, KDE Plasma, Cinnamon, Xfce and others. Many distributions offer several. Compare in <a href="guide-choosing-a-linux-distribution.html">choosing a Linux distribution</a>.</p>"""),
]
