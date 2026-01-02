# mas-dotfiles
My personal configuration of Omarchy Linux dotfiles. This doesn't contain my whole setup, since I've also modified system stuff like the plymouth and limine as well. But here's a screenshot of what it currently looks like:

<img width="2842" height="1440" alt="Screenshot" src="https://github.com/user-attachments/assets/3a411c87-050c-446e-995a-b1ee79b5d799" />

## Features
* Integration with [Markus' computer stuff](https://github.com/MarkusMaal/Markuse-asjad-next) system (Markuse arvuti asjad)
* Limit width of windows (because super-ultrawide master race)
* Custom eww widgets (shortcuts on the desktop and logo at the bottom)
* Modified lock screen appearance (hyprlock)
* Custom theme for fresh and nano TUI editors
* DDC/CI monitor brightness adjustment (waybar and binds, not useful for eDP displays)
* Custom hyprbars configuration
* Other tweaks and stuff I can't immediately recall

## Prerequisites
* Base [Omarchy Linux](https://omarchy.org/) installation
* An installation of Markus' computer stuff system, including...
  * [mas-corefiles](https://github.com/MarkusMaal/mas-corefiles.git) (branch: linux) cloned to $HOME/.mas
  * Valid Verifile certificate (can be generated using [mas-juurariist](https://github.com/MarkusMaal/mas-juurariist))
  * [M.A.I.A. web server](https://github.com/MarkusMaal/mas_maia) cloned to $HOME/.mas/maia
  * [Markuse-asjad-next](https://github.com/MarkusMaal/Markuse-asjad-next) compiled and installed
* Windows 11 fonts (specifically Segoe UI and Segoe UI Semilight fonts) and [REM font](https://fonts.google.com/specimen/REM)
* [Chezmoi](https://www.chezmoi.io/) (for deploying/updating these dotfiles)
* [Fresh](https://sinelaw.github.io/fresh/) and nano TUI editors
* Package: extra/ddcutil (for monitor brightness adjustment)
* AUR package: [aur/eww](https://aur.archlinux.org/eww.git) (for widgets)

# Deployment
Once you meet the prerequisites, run the following command in terminal: `chezmoi init --apply https://github.com/MarkusMaal/mas-dotfiles.git`

To pull new changes from this repository after installing the dotfiles, run the following command instead: `chezmoi update -v`

You may need to restart your PC for changes to fully take affect.
