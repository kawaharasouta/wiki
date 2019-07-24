ssh_config
==========

ssh_keygen
-----------
::
  $ ssh-keygen -t rsa -b 4096 -C "kawahara6514@gmail.com"
  Enter file in which to save the key (/Users/khwarizmi/.ssh/id_rsa): <path to key>
  Enter passphrase (empty for no passphrase): <passphrase> ※ i recommend no passphrase.





gihub setting 
---------------
accsess github_keys_

copy public key
~~~~~~~~~~~~~~~~
::
  $ pbcopy < <path to public key>

config for git 
~~~~~~~~~~~~~~~~
::
  Host github
    HostName github.com
    User git










.. _github_keys: https://github.com/settings/keys


