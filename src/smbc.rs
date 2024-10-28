// import remotefs trait and client
// Refer https://lib.rs/crates/remotefs-smb
use remotefs::{RemoteFs, fs::UnixPex};
use remotefs_smb::{SmbFs, SmbCredentials};
use std::path::Path;
use std::io::Read;


pub fn upload(){
    let mut client = SmbFs::new(
        SmbCredentials::new("192.168.56.110", "develop")
            .username("thomas")
            .password("thomas")
    );
    // connect
    assert!(client.connect().is_ok());
    // get working directory
    println!("Workdir: {}", client.pwd().ok().unwrap().display());
    // make directory
    assert!(client.create_dir(Path::new("\\cargo"), UnixPex::from(0o755)).is_ok());
    // change working directory
    assert!(client.change_dir(Path::new("\\cargo")).is_ok());

    let mut local_file = std::fs::File::open("C:\\workspace\\ProductSpace\\08-伟测-RPA\\3.开发实施\\updateFiles\\update-agent-XP.bat");

    // let local_file = File::open("C:\\workspace\\ProductSpace\\08-伟测-RPA\\3.开发实施\\updateFiles\\update-agent-XP.bat")?;
    let remote_path = "/cargo/update-agent-XP.bat";

    // let mut buffer: Vec<T> = Vec::new();
    // local_file.read_to_end(&mut buffer);
    let mut remote_file = client.open(Path::new(remote_path));
    // remote_file.write_all(&buffer)?;
    // client.copy(&mut self, local_file, remote_path);
    // client.copy(&mut self, /* &std::path::Path */);

    // assert!(client.copy(Path::new("\\cargo")).is_ok());
    // disconnect
    assert!(client.disconnect().is_ok());
}
