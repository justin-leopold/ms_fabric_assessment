from .audit import Audit
import sys

if __name__ == '__main__':
     
     audit = Audit()

     sp_info = {}
     args_valid = False
     for arg in sys.argv[1:]:
          if arg == '-l':
               collectors = audit.list_collectors()
               print(f'Supported collectors: {", ".join(collectors)}')
               continue 
          
          next_arg = sys.argv[sys.argv.index(arg)+1] if len(sys.argv) > sys.argv.index(arg)+1 else None
          if next_arg is not None:
               if arg == '-s':
                    audit.skip_collectors([c.strip() for c in next_arg.split(',')])
               elif arg == '-i':
                    audit.skip_other_collectors([c.strip() for c in next_arg.split(',')])
               elif arg == '-f':
                    audit.set_flags([f.strip() for f in next_arg.split(',')])
               elif arg == '-c':
                    audit.set_sink(next_arg)
                    args_valid = True
               elif arg == '-a':
                    audit.set_authentication(next_arg)
               elif arg == '-m':
                    audit.context.set_capacity_metrics_dataset(next_arg)
               elif arg == '-e':
                    audit.set_environment(next_arg)
               elif arg == '-sp':
                    sp_info['client_id'] = next_arg
               elif arg == '-spt':
                    sp_info['tenant_id'] = next_arg
               elif arg == '-sps':
                    sp_info['client_secret'] = next_arg
     
     
     if args_valid and len(sp_info) > 0:
          for key in sp_info.keys():
               if sp_info[key] is None:
                    args_valid = False
          
          if args_valid:
               audit.context.set_service_principal(sp_info['tenant_id'], sp_info['client_id'], sp_info['client_secret'])


     if args_valid:
          audit.run()
     else:
          usage = f'''Usage: python -m fabric_audit [options]
               -c <sink connection string>   required   Set connection string or path.
               -s <comma-separated list of collectors to skip>   Skip listed collectors.
               -i <comma-separated list of collectors to include>     Only include listed collectors.
               -f <{', '.join(audit.context.supported_flags())}>   Collector flags
               -a <ManagedIdentity, ServicePrincipal, Interactive, FabricIdentity>   Defaults to Interactive.
               -e <Public, USGov, USGovHigh, USGovMil, Germany, China>     Defaults to Public.
               -m <capacity metrics semantic model id>
               -l list supported collectors
               -sp <service principal client id>
               -spt <service principal tenant id>
               -sps <service principal client secret>
          '''
          print(usage)