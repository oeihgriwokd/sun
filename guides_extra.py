"""Extra guides. Each: (slug, title, meta description, html body). lk(item, text) links to a product page."""
def more(lk):
    return [
("boot-menu-keys-by-brand", "Boot menu keys for Dell, HP, Lenovo, ASUS, Acer and more",
 "Which key opens the boot menu on Dell, HP, Lenovo, ASUS, Acer, MSI, Gigabyte, Samsung and Surface computers, so you can start from a USB drive.",
 """<p>To start a computer from a USB drive you usually press one key as it powers on. The key depends on the brand. These are the common ones; if yours differs, a hint is often shown on the first start-up screen.</p>
<h2>Common boot menu keys</h2>
<ul><li><strong>Dell:</strong> F12</li><li><strong>HP:</strong> Esc, then F9 (some models use F9 directly)</li><li><strong>Lenovo:</strong> F12, or the small Novo button on some laptops</li><li><strong>ASUS:</strong> Esc or F8</li><li><strong>Acer:</strong> F12 (it may need to be enabled in BIOS first)</li><li><strong>MSI:</strong> F11</li><li><strong>Gigabyte and Aorus:</strong> F12</li><li><strong>Samsung:</strong> Esc or F10</li><li><strong>Microsoft Surface:</strong> hold the volume down button while powering on</li></ul>
<h2>Tips</h2>
<ul><li>Tap the key repeatedly right after pressing the power button, rather than holding it.</li><li>If Windows starts instead, shut down fully (hold Shift while choosing Shut down) and try again.</li><li>Intel-based Macs use the Option key at start-up. Newer Apple silicon Macs cannot start a standard Linux USB drive.</li></ul>
<p>Full walkthrough: <a href="guide-how-to-boot-from-usb.html">how to boot from a USB drive</a>. Ready to try something? See {lk('800016537860','Ubuntu')} or {lk('800016421272','Linux Mint')}.</p>"""),
("how-to-install-linux-from-usb", "How to install Linux from a USB drive",
 "A clear step-by-step guide to installing Linux from a bootable USB drive, from backing up to the first restart.",
 """<p>Installing Linux from a USB drive takes about 20 to 40 minutes on most computers. The steps below apply to most beginner-friendly distributions. Screens differ a little between systems.</p>
<h2>Before you begin</h2>
<ul><li>Back up your files to an external drive or cloud storage.</li><li>Plug a laptop into power.</li><li>Decide whether to replace your current system or keep it (see <a href="guide-how-to-dual-boot-linux-and-windows.html">dual booting</a>).</li></ul>
<h2>Steps</h2>
<ol><li>Insert the USB drive and <a href="guide-how-to-boot-from-usb.html">boot from it</a>.</li><li>Choose to try the system first (live mode) or go straight to Install.</li><li>Pick your language, keyboard layout and Wi-Fi network.</li><li>Choose the install type: erase the disk and install Linux, or install alongside your current system.</li><li>Set your time zone (pick the city nearest to you), name, computer name and password.</li><li>Wait for the files to copy, then restart when asked and remove the USB drive.</li></ol>
<h2>After installing</h2>
<p>Run the software updater, connect your printer and check that Wi-Fi, sound and graphics work. If you want a system with an easy installer, look at {lk('800016537860','Ubuntu')}, {lk('800016421272','Linux Mint')} or {lk('800034663198','Zorin OS')}.</p>"""),
("how-to-dual-boot-linux-and-windows", "How to dual boot Linux and Windows",
 "What dual booting means, what to prepare, and the safe steps for putting Linux beside Windows on one computer.",
 """<p>Dual booting lets you keep Windows and add Linux on the same computer. At start-up you choose which one to use. It is a good way to try Linux for real without giving up Windows.</p>
<h2>What to prepare</h2>
<ul><li>A full backup. Changing partitions always carries some risk.</li><li>Free disk space. Around 40 GB is a comfortable minimum for Linux plus your files.</li><li>Your BitLocker recovery key if Windows disk encryption is on.</li><li>In Windows, turn off Fast Startup so the disk is fully released.</li></ul>
<h2>Steps</h2>
<ol><li>Boot from your Linux USB drive.</li><li>Start the installer and choose the option to install alongside Windows.</li><li>Use the slider to set how much space Linux gets.</li><li>Finish the install and restart. A menu will let you pick Linux or Windows.</li></ol>
<h2>Good to know</h2>
<ul><li>A separate second drive for Linux is the safest setup.</li><li>Major Windows updates can sometimes change the boot menu. Keep your Linux USB drive handy to repair it.</li></ul>
<p>Related: <a href="guide-live-usb-or-install.html">live USB or install</a>, and <a href="guide-secure-boot-and-linux.html">Secure Boot and Linux</a>.</p>"""),
("best-linux-for-beginners", "Best Linux for beginners",
 "Easy Linux distributions for first-time users, what makes them beginner friendly, and how to try one safely from a USB drive.",
 """<p>The best Linux for a beginner is one with a friendly installer, a familiar desktop and plenty of online help. These are the usual recommendations.</p>
<h2>Good starting points</h2>
<ul><li>{lk('800016421272','Linux Mint')}: a traditional desktop with a start menu, popular with people coming from Windows.</li><li>{lk('800016537860','Ubuntu')}: the most widely used desktop Linux, with a huge amount of guides and forum answers.</li><li>{lk('800034663198','Zorin OS')}: designed to look and feel familiar to Windows users.</li></ul>
<h2>What helps a beginner</h2>
<ul><li><strong>Live mode</strong> so you can try it before installing.</li><li><strong>Long-term support (LTS)</strong> releases that stay stable for years. See <a href="guide-lts-vs-regular-releases.html">LTS vs regular releases</a>.</li><li><strong>A graphical software store</strong> so you never need the command line for everyday apps.</li></ul>
<h2>Next steps</h2>
<p>Read <a href="guide-how-to-boot-from-usb.html">how to boot from USB</a>, try live mode, then install when you are comfortable. Compare two favourites in <a href="guide-ubuntu-vs-linux-mint.html">Ubuntu vs Linux Mint</a>.</p>"""),
("best-linux-for-old-laptops", "Best Linux for old laptops and low-spec PCs",
 "Lightweight Linux options that can bring an older laptop or low-memory PC back to useful life, and how to choose between them.",
 """<p>An older laptop that has become slow or can no longer run the latest Windows can often run a lightweight Linux system well. Lightweight systems use simpler desktops that need less memory and processing power.</p>
<h2>What to look for</h2>
<ul><li>A light desktop such as XFCE, LXQt, LXDE or MATE.</li><li>A 32-bit option only if your computer is very old; most computers from the last 15 years are 64-bit.</li><li>At least 2 GB of memory for a comfortable experience. Less is possible with the lightest systems.</li></ul>
<h2>Tips for older hardware</h2>
<ul><li>Fitting a solid-state drive does more for speed than any software change.</li><li>Try live mode first to check Wi-Fi and graphics work before you install.</li><li>Browse our <a href="category-linux.html">Linux USB drives</a> and look for XFCE, LXQt, LXDE, MX or Q4OS in the name.</li></ul>
<p>New to Linux? See <a href="guide-best-linux-for-beginners.html">best Linux for beginners</a> and <a href="guide-how-to-install-linux-from-usb.html">how to install Linux from USB</a>.</p>"""),
("ubuntu-vs-linux-mint", "Ubuntu vs Linux Mint: which should you choose?",
 "A fair comparison of Ubuntu and Linux Mint for everyday use: desktop style, software, updates and who each suits.",
 """<p>Ubuntu and Linux Mint are two of the most popular desktop Linux systems. Mint is built on Ubuntu, so they share much underneath. The differences are mainly in the desktop and philosophy.</p>
<h2>Quick comparison</h2>
<ul><li><strong>Desktop:</strong> Mint's Cinnamon desktop looks like a classic Windows layout. Ubuntu uses a GNOME desktop with a dock on the side.</li><li><strong>Software:</strong> Both have a graphical software store. Ubuntu leans on Snap packages; Mint is more cautious about them.</li><li><strong>Support:</strong> Ubuntu LTS releases get long support and wide commercial backing. Mint LTS releases are also supported for years.</li><li><strong>Help online:</strong> Ubuntu has the larger community, and most Ubuntu answers also work on Mint.</li></ul>
<h2>Which suits you</h2>
<ul><li>Choose Mint if you want a familiar, traditional desktop.</li><li>Choose Ubuntu if you want the broadest support and a modern look.</li></ul>
<p>You can try either in live mode. See {lk('800016537860','Ubuntu')} and {lk('800016421272','Linux Mint')}, or read <a href="guide-choosing-a-linux-distribution.html">choosing a Linux distribution</a>.</p>"""),
("linux-for-windows-10-end-of-support", "Windows 10 has reached end of support: Linux as an option",
 "Windows 10 stopped getting free security updates in October 2025. Here is how Linux can keep a working computer in use.",
 """<p>Microsoft ended mainstream support for Windows 10 on 14 October 2025. Computers that cannot upgrade to Windows 11 are still able to run, but they no longer receive free security updates from Microsoft. Linux is one way to keep such a computer useful and supported.</p>
<h2>Your options</h2>
<ul><li>Upgrade to Windows 11 if your computer meets the requirements.</li><li>Pay for Microsoft's extended security updates, if eligible.</li><li>Move to a Linux system, which keeps receiving updates.</li></ul>
<h2>Trying Linux without risk</h2>
<ol><li>Back up your files.</li><li>Boot a Linux USB drive in live mode, which does not change your disk.</li><li>Check Wi-Fi, printing and the apps you use.</li><li>Install only when you are happy.</li></ol>
<p>Easy picks for Windows users: {lk('800016421272','Linux Mint')} and {lk('800034663198','Zorin OS')}. For lighter systems see <a href="guide-best-linux-for-old-laptops.html">Linux for old laptops</a>. Some software, such as certain games and Adobe tools, may not run on Linux, so check your needs first.</p>"""),
("what-is-persistence-on-a-live-usb", "What is persistence on a live USB?",
 "Persistence lets a live Linux USB drive keep your files and settings between restarts. Learn how it works and when to use it.",
 """<p>A normal live USB starts fresh each time: changes you make are lost when you shut down. Persistence adds a storage area on the USB drive so files, settings and installed apps can be kept.</p>
<h2>Why use it</h2>
<ul><li>Carry your own desktop and files on a drive between computers.</li><li>Use Linux on a computer without installing anything on its disk.</li><li>Keep a rescue toolkit with your own tools added.</li></ul>
<h2>Things to know</h2>
<ul><li>It is slower than an installed system because it runs from the USB drive.</li><li>A fast drive makes a big difference.</li><li>Back up important data. Removable drives can fail or be lost.</li></ul>
<p>Persistent options in our range include SanDisk cards in our <a href="category-sandisk.html">SD card category</a>. Compare with a full install in <a href="guide-live-usb-or-install.html">live USB or install</a>.</p>"""),
("uefi-vs-legacy-bios-boot", "UEFI vs Legacy BIOS: what it means for booting from USB",
 "The difference between UEFI and legacy BIOS boot modes, and how to choose the right option when booting a USB drive.",
 """<p>BIOS and UEFI are the firmware that starts your computer. Most computers made in the last decade use UEFI. Older ones use legacy BIOS, sometimes called CSM or Legacy mode.</p>
<h2>The practical difference</h2>
<ul><li><strong>UEFI</strong> supports large disks, faster start-up and Secure Boot. Modern installs use it.</li><li><strong>Legacy BIOS</strong> is the older method, still needed by some older computers and systems.</li></ul>
<h2>Which entry to pick</h2>
<p>In the boot menu a USB drive may appear twice. The entry with UEFI in its name starts in UEFI mode. Pick the UEFI entry on a modern computer. Use the plain entry on older computers.</p>
<h2>Keep modes consistent</h2>
<p>If Windows was installed in UEFI mode, install Linux in UEFI mode too. Mixing modes can cause boot problems.</p>
<p>See also <a href="guide-secure-boot-and-linux.html">Secure Boot and Linux</a> and <a href="guide-boot-menu-keys-by-brand.html">boot menu keys by brand</a>.</p>"""),
("secure-boot-and-linux", "Secure Boot and Linux: do you need to turn it off?",
 "What Secure Boot does, which Linux systems work with it, and what to check if a USB drive will not start.",
 """<p>Secure Boot is a UEFI feature that only lets approved software start. Many popular Linux distributions, including Ubuntu, Debian, Fedora and Linux Mint, support it. Some smaller systems and tools do not.</p>
<h2>If your USB drive will not start</h2>
<ol><li>Check the system's documentation to see if it supports Secure Boot.</li><li>Look for a security violation message at start-up. It usually means Secure Boot is blocking it.</li><li>If needed, open the UEFI settings and turn Secure Boot off, then try again.</li></ol>
<h2>Things to remember</h2>
<ul><li>Note the original setting so you can restore it.</li><li>Turning Secure Boot off lowers protection slightly, so turn it back on if the system supports it.</li><li>BitLocker on Windows may ask for a recovery key after the setting changes.</li></ul>
<p>Related: <a href="guide-uefi-vs-legacy-bios-boot.html">UEFI vs Legacy BIOS</a> and <a href="guide-how-to-boot-from-usb.html">how to boot from USB</a>.</p>"""),
("how-to-clone-a-disk-with-clonezilla", "How to clone a disk with Clonezilla",
 "A beginner guide to cloning or backing up a disk with Clonezilla from a bootable USB drive.",
 """<p>Clonezilla is a tool that copies a whole disk or partition to another disk or to an image file. Because it runs from a USB drive, it can copy a system that is not running.</p>
<h2>Common uses</h2>
<ul><li>Move to a bigger or faster drive.</li><li>Back up a full system before a big change.</li><li>Set up many computers from one image.</li></ul>
<h2>Basic steps</h2>
<ol><li>Connect your destination disk. It must be at least as large as the data you copy.</li><li>Boot from the {lk('800062044539','Clonezilla USB drive')}.</li><li>Choose device-to-device to clone directly, or device-to-image to make a backup file.</li><li>Pick the source and destination carefully, then confirm.</li></ol>
<h2>Warning</h2>
<p>The destination disk is overwritten. Always double-check which disk is which by name and size.</p>
<p>See also <a href="guide-recover-files-with-a-linux-usb.html">recovering files with a Linux USB</a>.</p>"""),
("recover-files-with-a-linux-usb", "How to recover files with a Linux USB drive",
 "Ways a bootable Linux USB drive can help you copy files off a computer that will not start, and what to avoid doing.",
 """<p>If a computer will not start, a bootable Linux USB drive can often still read its disk so you can copy your files to another drive.</p>
<h2>Steps</h2>
<ol><li>Plug in the Linux USB drive and an external drive for the rescued files.</li><li><a href="guide-how-to-boot-from-usb.html">Boot from the USB drive</a> in live mode.</li><li>Open the file manager and find the internal disk.</li><li>Copy your documents, photos and other files to the external drive.</li></ol>
<h2>Tips</h2>
<ul><li>Do not install anything or write to the failing disk.</li><li>If the disk makes unusual noises, stop and consult a data recovery service.</li><li>Encrypted disks need your password or key to open.</li></ul>
<p>Browse our <a href="category-tools.html">disk, rescue and security tools</a> or see <a href="guide-how-to-clone-a-disk-with-clonezilla.html">cloning with Clonezilla</a>.</p>"""),
("best-linux-for-gaming", "Best Linux for gaming",
 "What to look for in a Linux system for gaming, including Steam, Proton, graphics drivers and handheld PCs.",
 """<p>Gaming on Linux has improved a lot. Steam can run many Windows games on Linux using Proton, and native Linux games are common too.</p>
<h2>What matters</h2>
<ul><li><strong>Up to date graphics drivers</strong> for AMD, Intel or Nvidia.</li><li><strong>Steam</strong> installed and Proton enabled.</li><li><strong>A recent kernel</strong> for newer hardware.</li></ul>
<h2>Systems gamers often choose</h2>
<ul><li>Gaming-focused distributions such as Nobara, which come with many tools set up.</li><li>Beginner-friendly systems such as {lk('800016537860','Ubuntu')} or {lk('800016421272','Linux Mint')}.</li><li>Steam-handheld options; see our <a href="category-linux.html">Linux category</a>.</li></ul>
<p>Not every game runs, especially some with anti-cheat. Check ProtonDB before buying a game. See also our <a href="category-installers.html">app and game installer USB drives</a>.</p>"""),
("what-is-ventoy", "What is Ventoy and why use it?",
 "Ventoy turns one USB drive into a multi-boot drive. Learn how it works and when it is useful.",
 """<p>Ventoy is a tool that sets up a USB drive so you can boot many different system images from it. You copy ISO files to the drive like ordinary files, and Ventoy shows a menu at start-up.</p>
<h2>Why people use it</h2>
<ul><li>One drive holds several Linux systems and tools.</li><li>No need to rewrite the drive for each system.</li><li>Easy to add or remove images later.</li></ul>
<h2>Limits</h2>
<ul><li>A small number of images may not boot correctly, so test the ones you need.</li><li>It does not replace a full install.</li></ul>
<p>See the <a href="category-bundles.html">USB drive bundles</a> and our Ventoy listings in <a href="category-tools.html">tools</a>.</p>"""),
("raspberry-pi-os-microsd-guide", "Raspberry Pi OS on a microSD card: getting started",
 "How to start a Raspberry Pi from a prepared microSD card, what size you need and what to check first.",
 """<p>A Raspberry Pi starts from a microSD card rather than a built-in disk. A card with Raspberry Pi OS already on it lets you start quickly.</p>
<h2>Getting started</h2>
<ol><li>Power the Pi off and insert the card.</li><li>Connect a screen, keyboard and mouse.</li><li>Connect power and wait for the first start-up screen.</li><li>Follow the setup wizard for language, Wi-Fi and updates.</li></ol>
<h2>Check before buying</h2>
<ul><li>Your model of Pi, and whether the card supports its 32-bit or 64-bit mode.</li><li>Card size for your projects.</li><li>A good power supply, which prevents many odd problems.</li></ul>
<p>See our <a href="category-sandisk.html">bootable SD and microSD cards</a> and the guide to <a href="guide-what-is-persistence-on-a-live-usb.html">persistence</a>.</p>"""),
("lts-vs-regular-releases", "LTS vs regular Linux releases",
 "What LTS (long-term support) means for Linux, and when a regular release is a better fit.",
 """<p>LTS stands for long-term support. An LTS release receives security fixes for several years, which makes it a stable choice for everyday computers.</p>
<h2>LTS releases</h2>
<ul><li>Fewer big changes, so fewer surprises.</li><li>Security updates for years.</li><li>Best for family computers, work and servers.</li></ul>
<h2>Regular releases</h2>
<ul><li>Newer software and drivers sooner.</li><li>Shorter support, so you need to upgrade more often.</li><li>Good for new hardware and enthusiasts.</li></ul>
<p>Ubuntu offers both. See our <a href="category-linux.html">Linux USB drives</a> to compare, and <a href="guide-choosing-a-linux-distribution.html">choosing a distribution</a>.</p>"""),
("wipe-a-hard-drive-with-dban", "How to securely wipe a hard drive before selling",
 "How a bootable disk-wiping tool such as DBAN erases a hard drive, and what to know about SSDs.",
 """<p>Deleting files or formatting does not always remove data for good. A disk-wiping tool overwrites the whole drive so the old data is very hard to recover.</p>
<h2>Steps</h2>
<ol><li>Back up anything you want to keep.</li><li>Boot from a wiping tool such as DBAN on a USB drive.</li><li>Select the correct disk.</li><li>Choose a wipe method and start. Large drives can take hours.</li></ol>
<h2>Important</h2>
<ul><li>Wiping is permanent. Double-check the disk.</li><li>DBAN is designed for traditional hard drives. SSDs use different methods such as secure erase.</li></ul>
<p>See our <a href="category-tools.html">disk, rescue and security tools</a>.</p>"""),
("is-linux-safe-to-use", "Is Linux safe to use?",
 "Answers to common questions about Linux safety, viruses, updates and software for new users.",
 """<p>Linux is widely used on servers, phones and desktops, and security fixes arrive quickly through regular updates.</p>
<h2>Staying safe</h2>
<ul><li>Keep the system updated using the built-in updater.</li><li>Install software from the official software store.</li><li>Malware aimed at Linux desktops is less common than for Windows, but no system is immune.</li><li>Back up your files, whatever system you use.</li></ul>
<h2>Can I run my usual programs?</h2>
<ul><li>Web browsers, office tools, media players and many creative apps work well.</li><li>Some Windows-only programs do not run, so check first.</li></ul>
<p>Try without commitment: see <a href="guide-live-usb-or-install.html">live USB or install</a> and <a href="guide-best-linux-for-beginners.html">best Linux for beginners</a>.</p>"""),
]
