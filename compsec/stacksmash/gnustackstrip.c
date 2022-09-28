#include <elf.h>
#include <stdio.h>

int main(int argc, char* argv[]){
    if (argc < 2){
        printf("Usage ./gnustackstrip <elf file>\n");
        return 1;
    }
    
    FILE* orgbin = fopen(argv[1], "r+b");
    if(orgbin){
        unsigned char identifier[EI_NIDENT];
        fread(identifier, EI_NIDENT, 1, orgbin);
        fseek(orgbin, 0, 0);
        
        if( identifier[0] != ELFMAG0 ||
            identifier[1] != ELFMAG1 ||
            identifier[2] != ELFMAG2 ||
            identifier[3] != ELFMAG3){
            printf("Invalid ELF file\n");
            fclose(orgbin);
            return 2;
        }
            
        if(identifier[4] != ELFCLASS32){
            printf("Not 32 bit executable\n");
            fclose(orgbin);
            return 2;
        }
            
        Elf32_Ehdr header;
        fread(&header, sizeof(header), 1, orgbin);
        
        if (header.e_phoff != 0 &&
            header.e_phnum != 0 &&
            header.e_phentsize == sizeof(Elf32_Phdr)){
            
            fseek(orgbin, header.e_phoff, 0);
            for (int i = 0; i < header.e_phnum; i++){
                Elf32_Phdr chdr;
                fread(&chdr, sizeof(chdr), 1, orgbin);
                if (chdr.p_type == PT_GNU_STACK){
                    fseek(orgbin, -sizeof(chdr), 1);
                    chdr.p_type = PT_NULL;
                    fwrite(&chdr, sizeof(chdr), 1, orgbin);
                    fflush(orgbin);
                }
            }
        } else {
            printf("Warning: No ELF headers found!\n");
        }
        fclose(orgbin);
    } else {
        printf("Could not open file\n");
    }
    return 0;   
}
