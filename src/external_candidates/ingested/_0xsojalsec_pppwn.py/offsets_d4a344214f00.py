# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PPPwn\offsets.py
# Copyright (C) 2024 Andy Nguyen
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.


# FW 7.50 / 7.51 / 7.50
class OffsetsFirmware_750_755:
    PPPOE_SOFTC_LIST = 0xFFFFFFFF8433FCD0

    KERNEL_MAP = 0xFFFFFFFF843405B8

    SETIDT = 0xFFFFFFFF825D9440

    KMEM_ALLOC = 0xFFFFFFFF823753E0
    KMEM_ALLOC_PATCH1 = 0xFFFFFFFF823754AC
    KMEM_ALLOC_PATCH2 = 0xFFFFFFFF823754B4

    MEMCPY = 0xFFFFFFFF8248F800

    # 0xffffffffe19d9cf9 : mov cr0, rsi ; ud2 ; mov eax, 1 ; ret
    MOV_CR0_RSI_UD2_MOV_EAX_1_RET = 0xFFFFFFFF825A2589

    SECOND_GADGET_OFF = 0x3B

    # 0xffffffff824095e7 : jmp qword ptr [rsi + 0x3b]
    FIRST_GADGET = 0xFFFFFFFF824095E7

    # 0xffffffff82c90516 : push rbp ; jmp qword ptr [rsi]
    PUSH_RBP_JMP_QWORD_PTR_RSI = 0xFFFFFFFF82C90516

    # 0xffffffff82565e21 : pop rbx ; pop r14 ; pop rbp ; jmp qword ptr [rsi + 0x10]
    POP_RBX_POP_R14_POP_RBP_JMP_QWORD_PTR_RSI_10 = 0xFFFFFFFF82565E21

    # 0xffffffff82949bc6 : lea rsp, [rsi + 0x20] ; repz ret
    LEA_RSP_RSI_20_REPZ_RET = 0xFFFFFFFF82949BC6

    # 0xffffffff826d62fa : add rsp, 0x28 ; pop rbp ; ret
    ADD_RSP_28_POP_RBP_RET = 0xFFFFFFFF826D62FA

    # 0xffffffff82599199 : add rsp, 0xb0 ; pop rbp ; ret
    ADD_RSP_B0_POP_RBP_RET = 0xFFFFFFFF82599199

    # 0xffffffff822008f3 : ret
    RET = 0xFFFFFFFF822008F3

    # 0xffffffff8228c0fc : pop rdi ; ret
    POP_RDI_RET = 0xFFFFFFFF8228C0FC

    # 0xffffffff82257b77 : pop rsi ; ret
    POP_RSI_RET = 0xFFFFFFFF82257B77

    # 0xffffffff822f2f1a : pop rdx ; ret
    POP_RDX_RET = 0xFFFFFFFF822F2F1A

    # 0xffffffff8231312c : pop rcx ; ret
    POP_RCX_RET = 0xFFFFFFFF8231312C

    # 0xffffffff82227fa7 : pop r8 ; pop rbp ; ret
    POP_R8_POP_RBP_RET = 0xFFFFFFFF82227FA7

    # 0xffffffff827dc32f : pop r12 ; ret
    POP_R12_RET = 0xFFFFFFFF827DC32F

    # 0xffffffff8231a01e : pop rax ; ret
    POP_RAX_RET = 0xFFFFFFFF8231A01E

    # 0xffffffff822008f2 : pop rbp ; ret
    POP_RBP_RET = 0xFFFFFFFF822008F2

    # 0xffffffff82bd096a : push rsp ; pop rsi ; ret
    PUSH_RSP_POP_RSI_RET = 0xFFFFFFFF82BD096A

    # 0xffffffff82447f40 : mov rdi, qword ptr [rdi] ; pop rbp ; jmp rax
    MOV_RDI_QWORD_PTR_RDI_POP_RBP_JMP_RAX = 0xFFFFFFFF82447F40

    # 0xffffffff82b8e5ae : mov byte ptr [rcx], al ; ret
    MOV_BYTE_PTR_RCX_AL_RET = 0xFFFFFFFF82B8E5AE

    # 0xffffffff8246ce59 : mov rdi, rbx ; call r12
    MOV_RDI_RBX_CALL_R12 = 0xFFFFFFFF8246CE59

    # 0xffffffff8246cc67 : mov rdi, r14 ; call r12
    MOV_RDI_R14_CALL_R12 = 0xFFFFFFFF8246CC67

    # 0xffffffff824cd8c1 : mov rsi, rbx ; call rax
    MOV_RSI_RBX_CALL_RAX = 0xFFFFFFFF824CD8C1

    # 0xffffffff824bdaa8 : mov r14, rax ; call r8
    MOV_R14_RAX_CALL_R8 = 0xFFFFFFFF824BDAA8

    # 0xffffffff82cd070a : add rdi, rcx ; ret
    ADD_RDI_RCX_RET = 0xFFFFFFFF82CD070A

    # 0xffffffff8235a377 : sub rsi, rdx ; mov rax, rsi ; pop rbp ; ret
    SUB_RSI_RDX_MOV_RAX_RSI_POP_RBP_RET = 0xFFFFFFFF8235A377

    # 0xffffffff8253f959 : jmp r14
    JMP_R14 = 0xFFFFFFFF8253F959


# FW 8.00 / 8.01 / 8.03
class OffsetsFirmware_800_803:
    PPPOE_SOFTC_LIST = 0xFFFFFFFF84422370

    KERNEL_MAP = 0xFFFFFFFF83D243E0

    SETIDT = 0xFFFFFFFF82249DD0

    KMEM_ALLOC = 0xFFFFFFFF8221B3F0
    KMEM_ALLOC_PATCH1 = 0xFFFFFFFF8221B4BC
    KMEM_ALLOC_PATCH2 = 0xFFFFFFFF8221B4C4

    MEMCPY = 0xFFFFFFFF8245E1C0

    # 0xffffffff82660609 : mov cr0, rsi ; ud2 ; mov eax, 1 ; ret
    MOV_CR0_RSI_UD2_MOV_EAX_1_RET = 0xFFFFFFFF82660609

    SECOND_GADGET_OFF = 0x3B

    # 0xffffffff82245f1d : jmp qword ptr [rsi + 0x3b]
    FIRST_GADGET = 0xFFFFFFFF82245F1D

    # 0xffffffff82c72e66 : push rbp ; jmp qword ptr [rsi]
    PUSH_RBP_JMP_QWORD_PTR_RSI = 0xFFFFFFFF82C72E66

    # 0xffffffff823b3311 : pop rbx ; pop r14 ; pop rbp ; jmp qword ptr [rsi + 0x10]
    POP_RBX_POP_R14_POP_RBP_JMP_QWORD_PTR_RSI_10 = 0xFFFFFFFF823B3311

    # 0xffffffff8293bb06 : lea rsp, [rsi + 0x20] ; repz ret
    LEA_RSP_RSI_20_REPZ_RET = 0xFFFFFFFF8293BB06

    # 0xffffffff826aeada : add rsp, 0x28 ; pop rbp ; ret
    ADD_RSP_28_POP_RBP_RET = 0xFFFFFFFF826AEADA

    # 0xffffffff8267b46f : add rsp, 0xb0 ; pop rbp ; ret
    ADD_RSP_B0_POP_RBP_RET = 0xFFFFFFFF8267B46F

    # 0xffffffff822008e0 : ret
    RET = 0xFFFFFFFF822008E0

    # 0xffffffff82652d81 : pop rdi ; ret
    POP_RDI_RET = 0xFFFFFFFF82652D81

    # 0xffffffff82212728 : pop rsi ; ret
    POP_RSI_RET = 0xFFFFFFFF82212728

    # 0xffffffff82482342 : pop rdx ; ret
    POP_RDX_RET = 0xFFFFFFFF82482342

    # 0xffffffff82233677 : pop rcx ; ret
    POP_RCX_RET = 0xFFFFFFFF82233677

    # 0xffffffff823ac6ed : pop r8 ; pop rbp ; ret
    POP_R8_POP_RBP_RET = 0xFFFFFFFF823AC6ED

    # 0xffffffff8279b42f : pop r12 ; ret
    POP_R12_RET = 0xFFFFFFFF8279B42F

    # 0xffffffff8223711d : pop rax ; ret
    POP_RAX_RET = 0xFFFFFFFF8223711D

    # 0xffffffff822008df : pop rbp ; ret
    POP_RBP_RET = 0xFFFFFFFF822008DF

    # 0xffffffff82bb35ba : push rsp ; pop rsi ; ret
    PUSH_RSP_POP_RSI_RET = 0xFFFFFFFF82BB35BA

    # 0xffffffff82529060 : mov rdi, qword ptr [rdi] ; pop rbp ; jmp rax
    MOV_RDI_QWORD_PTR_RDI_POP_RBP_JMP_RAX = 0xFFFFFFFF82529060

    # 0xffffffff82b7124e : mov byte ptr [rcx], al ; ret
    MOV_BYTE_PTR_RCX_AL_RET = 0xFFFFFFFF82B7124E

    # 0xffffffff8232e9ac : mov rdi, rbx ; call r12
    MOV_RDI_RBX_CALL_R12 = 0xFFFFFFFF8232E9AC

    # 0xffffffff8232e7e7 : mov rdi, r14 ; call r12
    MOV_RDI_R14_CALL_R12 = 0xFFFFFFFF8232E7E7

    # 0xffffffff823d049e : mov rsi, rbx ; call rax
    MOV_RSI_RBX_CALL_RAX = 0xFFFFFFFF823D049E

    # 0xffffffff825dc638 : mov r14, rax ; call r8
    MOV_R14_RAX_CALL_R8 = 0xFFFFFFFF825DC638

    # 0xffffffff82cb305a : add rdi, rcx ; ret
    ADD_RDI_RCX_RET = 0xFFFFFFFF82CB305A

    # 0xffffffff8266f467 : sub rsi, rdx ; mov rax, rsi ; pop rbp ; ret
    SUB_RSI_RDX_MOV_RAX_RSI_POP_RBP_RET = 0xFFFFFFFF8266F467

    # 0xffffffff82b82393 : jmp r14
    JMP_R14 = 0xFFFFFFFF82B82393


# FW 8.50 / 8.52
class OffsetsFirmware_850_852:
    PPPOE_SOFTC_LIST = 0xFFFFFFFF83DD6018

    KERNEL_MAP = 0xFFFFFFFF83E64228

    SETIDT = 0xFFFFFFFF82467340

    KMEM_ALLOC = 0xFFFFFFFF824199A0
    KMEM_ALLOC_PATCH1 = 0xFFFFFFFF82419A6C
    KMEM_ALLOC_PATCH2 = 0xFFFFFFFF82419A74

    MEMCPY = 0xFFFFFFFF825A40F0

    # 0xffffffff823ce849 : mov cr0, rsi ; ud2 ; mov eax, 1 ; ret
    MOV_CR0_RSI_UD2_MOV_EAX_1_RET = 0xFFFFFFFF823CE849

    SECOND_GADGET_OFF = 0x3B

    # 0xffffffff8237e09d : jmp qword ptr [rsi + 0x3b]
    FIRST_GADGET = 0xFFFFFFFF8237E09D

    # 0xffffffff82c766e6 : push rbp ; jmp qword ptr [rsi]
    PUSH_RBP_JMP_QWORD_PTR_RSI = 0xFFFFFFFF82C766E6

    # 0xffffffff822a3a31 : pop rbx ; pop r14 ; pop rbp ; jmp qword ptr [rsi + 0x10]
    POP_RBX_POP_R14_POP_RBP_JMP_QWORD_PTR_RSI_10 = 0xFFFFFFFF822A3A31

    # 0xffffffff829261c6 : lea rsp, [rsi + 0x20] ; repz ret
    LEA_RSP_RSI_20_REPZ_RET = 0xFFFFFFFF829261C6

    # 0xffffffff826d2a8a : add rsp, 0x28 ; pop rbp ; ret
    ADD_RSP_28_POP_RBP_RET = 0xFFFFFFFF826D2A8A

    # 0xffffffff82439c6f : add rsp, 0xb0 ; pop rbp ; ret
    ADD_RSP_B0_POP_RBP_RET = 0xFFFFFFFF82439C6F

    # 0xffffffff822008e0 : ret
    RET = 0xFFFFFFFF822008E0

    # 0xffffffff825dc87d : pop rdi ; ret
    POP_RDI_RET = 0xFFFFFFFF825DC87D

    # 0xffffffff823882c9 : pop rsi ; ret
    POP_RSI_RET = 0xFFFFFFFF823882C9

    # 0xffffffff8232eec2 : pop rdx ; ret
    POP_RDX_RET = 0xFFFFFFFF8232EEC2

    # 0xffffffff82246d0c : pop rcx ; ret
    POP_RCX_RET = 0xFFFFFFFF82246D0C

    # 0xffffffff8237cd26 : pop r8 ; pop rbp ; ret
    POP_R8_POP_RBP_RET = 0xFFFFFFFF8237CD26

    # 0xffffffff827a366f : pop r12 ; ret
    POP_R12_RET = 0xFFFFFFFF827A366F

    # 0xffffffff82202d74 : pop rax ; ret
    POP_RAX_RET = 0xFFFFFFFF82202D74

    # 0xffffffff822008df : pop rbp ; ret
    POP_RBP_RET = 0xFFFFFFFF822008DF

    # 0xffffffff82bb5866 : push rsp ; pop rsi ; ret
    PUSH_RSP_POP_RSI_RET = 0xFFFFFFFF82BB5866

    # 0xffffffff82444180 : mov rdi, qword ptr [rdi] ; pop rbp ; jmp rax
    MOV_RDI_QWORD_PTR_RDI_POP_RBP_JMP_RAX = 0xFFFFFFFF82444180

    # 0xffffffff82b73476 : mov byte ptr [rcx], al ; ret
    MOV_BYTE_PTR_RCX_AL_RET = 0xFFFFFFFF82B73476

    # 0xffffffff8220fbbc : mov rdi, rbx ; call r12
    MOV_RDI_RBX_CALL_R12 = 0xFFFFFFFF8220FBBC

    # 0xffffffff8220f9f7 : mov rdi, r14 ; call r12
    MOV_RDI_R14_CALL_R12 = 0xFFFFFFFF8220F9F7

    # 0xffffffff8253628e : mov rsi, rbx ; call rax
    MOV_RSI_RBX_CALL_RAX = 0xFFFFFFFF8253628E

    # 0xffffffff825bb768 : mov r14, rax ; call r8
    MOV_R14_RAX_CALL_R8 = 0xFFFFFFFF825BB768

    # 0xffffffff82cb68da : add rdi, rcx ; ret
    ADD_RDI_RCX_RET = 0xFFFFFFFF82CB68DA

    # 0xffffffff82346e67 : sub rsi, rdx ; mov rax, rsi ; pop rbp ; ret
    SUB_RSI_RDX_MOV_RAX_RSI_POP_RBP_RET = 0xFFFFFFFF82346E67

    # 0xffffffff82b845c7 : jmp r14
    JMP_R14 = 0xFFFFFFFF82B845C7


# FW 9.00
class OffsetsFirmware_900:
    PPPOE_SOFTC_LIST = 0xFFFFFFFF843ED9F8

    KERNEL_MAP = 0xFFFFFFFF84468D48

    SETIDT = 0xFFFFFFFF82512C40

    KMEM_ALLOC = 0xFFFFFFFF8257BE70
    KMEM_ALLOC_PATCH1 = 0xFFFFFFFF8257BF3C
    KMEM_ALLOC_PATCH2 = 0xFFFFFFFF8257BF44

    MEMCPY = 0xFFFFFFFF824714B0

    # 0xffffffff823fb949 : mov cr0, rsi ; ud2 ; mov eax, 1 ; ret
    MOV_CR0_RSI_UD2_MOV_EAX_1_RET = 0xFFFFFFFF823FB949

    SECOND_GADGET_OFF = 0x3D

    # 0xffffffff82996603 : jmp qword ptr [rsi + 0x3d]
    FIRST_GADGET = 0xFFFFFFFF82996603

    # 0xffffffff82c76646 : push rbp ; jmp qword ptr [rsi]
    PUSH_RBP_JMP_QWORD_PTR_RSI = 0xFFFFFFFF82C76646

    # 0xffffffff822b4151 : pop rbx ; pop r14 ; pop rbp ; jmp qword ptr [rsi + 0x10]
    POP_RBX_POP_R14_POP_RBP_JMP_QWORD_PTR_RSI_10 = 0xFFFFFFFF822B4151

    # 0xffffffff82941e46 : lea rsp, [rsi + 0x20] ; repz ret
    LEA_RSP_RSI_20_REPZ_RET = 0xFFFFFFFF82941E46

    # 0xffffffff826c52aa : add rsp, 0x28 ; pop rbp ; ret
    ADD_RSP_28_POP_RBP_RET = 0xFFFFFFFF826C52AA

    # 0xffffffff8251b08f : add rsp, 0xb0 ; pop rbp ; ret
    ADD_RSP_B0_POP_RBP_RET = 0xFFFFFFFF8251B08F

    # 0xffffffff822008e0 : ret
    RET = 0xFFFFFFFF822008E0

    # 0xffffffff822391a8 : pop rdi ; ret
    POP_RDI_RET = 0xFFFFFFFF822391A8

    # 0xffffffff822aad39 : pop rsi ; ret
    POP_RSI_RET = 0xFFFFFFFF822AAD39

    # 0xffffffff82322eba : pop rdx ; ret
    POP_RDX_RET = 0xFFFFFFFF82322EBA

    # 0xffffffff822445e7 : pop rcx ; ret
    POP_RCX_RET = 0xFFFFFFFF822445E7

    # 0xffffffff822ab4dd : pop r8 ; pop rbp ; ret
    POP_R8_POP_RBP_RET = 0xFFFFFFFF822AB4DD

    # 0xffffffff8279fa0f : pop r12 ; ret
    POP_R12_RET = 0xFFFFFFFF8279FA0F

    # 0xffffffff82234ec8 : pop rax ; ret
    POP_RAX_RET = 0xFFFFFFFF82234EC8

    # 0xffffffff822008df : pop rbp ; ret
    POP_RBP_RET = 0xFFFFFFFF822008DF

    # 0xffffffff82bb687a : push rsp ; pop rsi ; ret
    PUSH_RSP_POP_RSI_RET = 0xFFFFFFFF82BB687A

    # 0xffffffff82244ed0 : mov rdi, qword ptr [rdi] ; pop rbp ; jmp rax
    MOV_RDI_QWORD_PTR_RDI_POP_RBP_JMP_RAX = 0xFFFFFFFF82244ED0

    # 0xffffffff82b7450e : mov byte ptr [rcx], al ; ret
    MOV_BYTE_PTR_RCX_AL_RET = 0xFFFFFFFF82B7450E

    # 0xffffffff82632b9c : mov rdi, rbx ; call r12
    MOV_RDI_RBX_CALL_R12 = 0xFFFFFFFF82632B9C

    # 0xffffffff8235b387 : mov rdi, r14 ; call r12
    MOV_RDI_R14_CALL_R12 = 0xFFFFFFFF8235B387

    # 0xffffffff822e3d7e : mov rsi, rbx ; call rax
    MOV_RSI_RBX_CALL_RAX = 0xFFFFFFFF822E3D7E

    # 0xffffffff82363918 : mov r14, rax ; call r8
    MOV_R14_RAX_CALL_R8 = 0xFFFFFFFF82363918

    # 0xffffffff82cb683a : add rdi, rcx ; ret
    ADD_RDI_RCX_RET = 0xFFFFFFFF82CB683A

    # 0xffffffff82409557 : sub rsi, rdx ; mov rax, rsi ; pop rbp ; ret
    SUB_RSI_RDX_MOV_RAX_RSI_POP_RBP_RET = 0xFFFFFFFF82409557

    # 0xffffffff82b85693 : jmp r14
    JMP_R14 = 0xFFFFFFFF82B85693


# FW 9.03 / 9.04
class OffsetsFirmware_903_904:
    PPPOE_SOFTC_LIST = 0xFFFFFFFF843E99F8

    KERNEL_MAP = 0xFFFFFFFF84464D48
    SETIDT = 0xFFFFFFFF825128E0

    KMEM_ALLOC = 0xFFFFFFFF8257A070
    KMEM_ALLOC_PATCH1 = 0xFFFFFFFF8257A13C
    KMEM_ALLOC_PATCH2 = 0xFFFFFFFF8257A144

    MEMCPY = 0xFFFFFFFF82471130

    # 0xffffffff823fb679 : mov cr0, rsi ; ud2 ; mov eax, 1 ; ret
    MOV_CR0_RSI_UD2_MOV_EAX_1_RET = 0xFFFFFFFF823FB679

    SECOND_GADGET_OFF = 0x3D

    # 0xffffffff829e686f : jmp qword ptr [rsi + 0x3d]
    FIRST_GADGET = 0xFFFFFFFF829E686F

    # 0xffffffff82c74566 : push rbp ; jmp qword ptr [rsi]
    PUSH_RBP_JMP_QWORD_PTR_RSI = 0xFFFFFFFF82C74566

    # 0xffffffff822b4151 : pop rbx ; pop r14 ; pop rbp ; jmp qword ptr [rsi + 0x10]
    POP_RBX_POP_R14_POP_RBP_JMP_QWORD_PTR_RSI_10 = 0xFFFFFFFF822B4151

    # 0xffffffff8293fe06 : lea rsp, [rsi + 0x20] ; repz ret
    LEA_RSP_RSI_20_REPZ_RET = 0xFFFFFFFF8293FE06

    # 0xffffffff826c31aa : add rsp, 0x28 ; pop rbp ; ret
    ADD_RSP_28_POP_RBP_RET = 0xFFFFFFFF826C31AA

    # 0xffffffff8251ad2f : add rsp, 0xb0 ; pop rbp ; ret
    ADD_RSP_B0_POP_RBP_RET = 0xFFFFFFFF8251AD2F

    # 0xffffffff822008e0 : ret
    RET = 0xFFFFFFFF822008E0

    # 0xffffffff8238e75d : pop rdi ; ret
    POP_RDI_RET = 0xFFFFFFFF8238E75D

    # 0xffffffff822aad39 : pop rsi ; ret
    POP_RSI_RET = 0xFFFFFFFF822AAD39

    # 0xffffffff8244cc56 : pop rdx ; ret
    POP_RDX_RET = 0xFFFFFFFF8244CC56

    # 0xffffffff822445e7 : pop rcx ; ret
    POP_RCX_RET = 0xFFFFFFFF822445E7

    # 0xffffffff822ab4dd : pop r8 ; pop rbp ; ret
    POP_R8_POP_RBP_RET = 0xFFFFFFFF822AB4DD

    # 0xffffffff8279d9cf : pop r12 ; ret
    POP_R12_RET = 0xFFFFFFFF8279D9CF

    # 0xffffffff82234ec8 : pop rax ; ret
    POP_RAX_RET = 0xFFFFFFFF82234EC8

    # 0xffffffff822008df : pop rbp ; ret
    POP_RBP_RET = 0xFFFFFFFF822008DF

    # 0xffffffff82bb479a : push rsp ; pop rsi ; ret
    PUSH_RSP_POP_RSI_RET = 0xFFFFFFFF82BB479A

    # 0xffffffff82244ed0 : mov rdi, qword ptr [rdi] ; pop rbp ; jmp rax
    MOV_RDI_QWORD_PTR_RDI_POP_RBP_JMP_RAX = 0xFFFFFFFF82244ED0

    # 0xffffffff825386d8 : mov byte ptr [rcx], al ; ret
    MOV_BYTE_PTR_RCX_AL_RET = 0xFFFFFFFF825386D8

    # 0xffffffff82630b0c : mov rdi, rbx ; call r12
    MOV_RDI_RBX_CALL_R12 = 0xFFFFFFFF82630B0C

    # 0xffffffff8235b337 : mov rdi, r14 ; call r12
    MOV_RDI_R14_CALL_R12 = 0xFFFFFFFF8235B337

    # 0xffffffff822e3d2e : mov rsi, rbx ; call rax
    MOV_RSI_RBX_CALL_RAX = 0xFFFFFFFF822E3D2E

    # 0xffffffff823638c8 : mov r14, rax ; call r8
    MOV_R14_RAX_CALL_R8 = 0xFFFFFFFF823638C8

    # 0xffffffff82cb475a : add rdi, rcx ; ret
    ADD_RDI_RCX_RET = 0xFFFFFFFF82CB475A

    # 0xffffffff82409287 : sub rsi, rdx ; mov rax, rsi ; pop rbp ; ret
    SUB_RSI_RDX_MOV_RAX_RSI_POP_RBP_RET = 0xFFFFFFFF82409287

    # 0xffffffff82b835b3 : jmp r14
    JMP_R14 = 0xFFFFFFFF82B835B3


# FW 9.50 / 9.51 / 9.60
class OffsetsFirmware_950_960:
    PPPOE_SOFTC_LIST = 0xFFFFFFFF8434C0A8

    KERNEL_MAP = 0xFFFFFFFF84347830

    SETIDT = 0xFFFFFFFF8254D320

    KMEM_ALLOC = 0xFFFFFFFF823889D0
    KMEM_ALLOC_PATCH1 = 0xFFFFFFFF82388A9C
    KMEM_ALLOC_PATCH2 = 0xFFFFFFFF82388AA4

    MEMCPY = 0xFFFFFFFF82401CC0

    MOV_CR0_RSI_UD2_MOV_EAX_1_RET = 0xFFFFFFFF822BEA79

    SECOND_GADGET_OFF = 0x3B

    # 0xffffffff822c53cd : jmp qword ptr [rsi + 0x3b]
    FIRST_GADGET = 0xFFFFFFFF822C53CD

    # 0xffffffff82c6ec06 : push rbp ; jmp qword ptr [rsi]
    PUSH_RBP_JMP_QWORD_PTR_RSI = 0xFFFFFFFF82C6EC06

    # 0xffffffff822bf041 : pop rbx ; pop r14 ; pop rbp ; jmp qword ptr [rsi + 0x10]
    POP_RBX_POP_R14_POP_RBP_JMP_QWORD_PTR_RSI_10 = 0xFFFFFFFF822BF041

    # 0xffffffff82935fc6 : lea rsp, [rsi + 0x20] ; repz ret
    LEA_RSP_RSI_20_REPZ_RET = 0xFFFFFFFF82935FC6

    # 0xffffffff826adfda : add rsp, 0x28 ; pop rbp ; ret
    ADD_RSP_28_POP_RBP_RET = 0xFFFFFFFF826ADFDA

    # 0xffffffff82584c1f : add rsp, 0xb0 ; pop rbp ; ret
    ADD_RSP_B0_POP_RBP_RET = 0xFFFFFFFF82584C1F

    # 0xffffffff822008e0 : ret
    RET = 0xFFFFFFFF822008E0

    # 0xffffffff82315161 : pop rdi ; ret
    POP_RDI_RET = 0xFFFFFFFF82315161

    # 0xffffffff822dd859 : pop rsi ; ret
    POP_RSI_RET = 0xFFFFFFFF822DD859

    # 0xffffffff822cad55 : pop rdx ; ret
    POP_RDX_RET = 0xFFFFFFFF822CAD55

    # 0xffffffff8222d707 : pop rcx ; ret
    POP_RCX_RET = 0xFFFFFFFF8222D707

    # 0xffffffff8220fec7 : pop r8 ; pop rbp ; ret
    POP_R8_POP_RBP_RET = 0xFFFFFFFF8220FEC7

    # 0xffffffff8279f14f : pop r12 ; ret
    POP_R12_RET = 0xFFFFFFFF8279F14F

    # 0xffffffff8223a7fe : pop rax ; ret
    POP_RAX_RET = 0xFFFFFFFF8223A7FE

    # 0xffffffff822008df : pop rbp ; ret
    POP_RBP_RET = 0xFFFFFFFF822008DF

    # 0xffffffff82bad912 : push rsp ; pop rsi ; ret
    PUSH_RSP_POP_RSI_RET = 0xFFFFFFFF82BAD912

    # 0xffffffff8235fea0 : mov rdi, qword ptr [rdi] ; pop rbp ; jmp rax
    MOV_RDI_QWORD_PTR_RDI_POP_RBP_JMP_RAX = 0xFFFFFFFF8235FEA0

    # 0xffffffff824f2458 : mov byte ptr [rcx], al ; ret
    MOV_BYTE_PTR_RCX_AL_RET = 0xFFFFFFFF824F2458

    # 0xffffffff822524dc : mov rdi, rbx ; call r12
    MOV_RDI_RBX_CALL_R12 = 0xFFFFFFFF822524DC

    # 0xffffffff82252317 : mov rdi, r14 ; call r12
    MOV_RDI_R14_CALL_R12 = 0xFFFFFFFF82252317

    # 0xffffffff824a07ae : mov rsi, rbx ; call rax
    MOV_RSI_RBX_CALL_RAX = 0xFFFFFFFF824A07AE

    # 0xffffffff82567228 : mov r14, rax ; call r8
    MOV_R14_RAX_CALL_R8 = 0xFFFFFFFF82567228

    # 0xffffffff82caedfa : add rdi, rcx ; ret
    ADD_RDI_RCX_RET = 0xFFFFFFFF82CAEDFA

    # 0xffffffff82333437 : sub rsi, rdx ; mov rax, rsi ; pop rbp ; ret
    SUB_RSI_RDX_MOV_RAX_RSI_POP_RBP_RET = 0xFFFFFFFF82333437

    # 0xffffffff82b7c6e7 : jmp r14
    JMP_R14 = 0xFFFFFFFF82B7C6E7


# FW 10.00 / 10.01
class OffsetsFirmware_1000_1001:
    PPPOE_SOFTC_LIST = 0xFFFFFFFF8446D920

    KERNEL_MAP = 0xFFFFFFFF8447BEF8

    SETIDT = 0xFFFFFFFF8227B460

    KMEM_ALLOC = 0xFFFFFFFF8253B040
    KMEM_ALLOC_PATCH1 = 0xFFFFFFFF8253B10C
    KMEM_ALLOC_PATCH2 = 0xFFFFFFFF8253B114

    MEMCPY = 0xFFFFFFFF82672D20

    # 0xffffffff82376089 : mov cr0 rsi ; ud2 ; mov eax 1; ret
    MOV_CR0_RSI_UD2_MOV_EAX_1_RET = 0xFFFFFFFF82376089

    SECOND_GADGET_OFF = 0x3B

    # 0xffffffff82249c5d : jmp qword ptr [rsi + 0x3b]
    FIRST_GADGET = 0xFFFFFFFF82249C5D

    # 0xffffffff82c73946 : push rbp ; jmp qword ptr [rsi]
    PUSH_RBP_JMP_QWORD_PTR_RSI = 0xFFFFFFFF82C73946

    # 0xffffffff82545741 : pop rbx ; pop r14 ; pop rbp ; jmp qword ptr [rsi + 0x10]
    POP_RBX_POP_R14_POP_RBP_JMP_QWORD_PTR_RSI_10 = 0xFFFFFFFF82545741

    # 0xffffffff8292b346 : lea rsp, [rsi + 0x20] ; repz ret
    LEA_RSP_RSI_20_REPZ_RET = 0xFFFFFFFF8292B346

    # 0xffffffff826d0d0a : add rsp, 0x28 ; pop rbp ; ret
    ADD_RSP_28_POP_RBP_RET = 0xFFFFFFFF826D0D0A

    # 0xffffffff82531c3f : add rsp, 0xb0 ; pop rbp ; ret
    ADD_RSP_B0_POP_RBP_RET = 0xFFFFFFFF82531C3F

    # 0xffffffff822008e0 : ret
    RET = 0xFFFFFFFF822008E0

    # 0xffffffff82510c4e : pop rdi ; ret
    POP_RDI_RET = 0xFFFFFFFF82510C4E

    # 0xffffffff822983e0 : pop rsi ; ret
    POP_RSI_RET = 0xFFFFFFFF822983E0

    # 0xffffffff824029b2 : pop rdx ; ret
    POP_RDX_RET = 0xFFFFFFFF824029B2

    # 0xffffffff822983ba : pop rcx ; ret
    POP_RCX_RET = 0xFFFFFFFF822983BA

    # 0xffffffff8237dd7d : pop r8 ; pop rbp ; ret
    POP_R8_POP_RBP_RET = 0xFFFFFFFF8237DD7D

    # 0xffffffff827b32ef : pop r12 ; ret
    POP_R12_RET = 0xFFFFFFFF827B32EF

    # 0xffffffff8229974f : pop rax ; ret
    POP_RAX_RET = 0xFFFFFFFF8229974F

    # 0xffffffff822008df : pop rbp ; ret
    POP_RBP_RET = 0xFFFFFFFF822008DF

    # 0xffffffff82bb3ee6 : push rsp ; pop rsi ; ret
    PUSH_RSP_POP_RSI_RET = 0xFFFFFFFF82BB3EE6

    # 0xffffffff8256bfb0 : mov rdi, qword ptr [rdi] ; pop rbp ; jmp rax
    MOV_RDI_QWORD_PTR_RDI_POP_RBP_JMP_RAX = 0xFFFFFFFF8256BFB0

    # 0xffffffff824f0448 : mov byte ptr [rcx], al ; ret
    MOV_BYTE_PTR_RCX_AL_RET = 0xFFFFFFFF824F0448

    # 0xffffffff8236bbec : mov rdi, rbx ; call r12
    MOV_RDI_RBX_CALL_R12 = 0xFFFFFFFF8236BBEC

    # 0xffffffff8236ba27 : mov rdi, r14 ; call r12
    MOV_RDI_R14_CALL_R12 = 0xFFFFFFFF8236BA27

    # 0xffffffff823f501e : mov rsi, rbx ; call rax
    MOV_RSI_RBX_CALL_RAX = 0xFFFFFFFF823F501E

    # 0xffffffff8259e638 : mov r14, rax ; call r8
    MOV_R14_RAX_CALL_R8 = 0xFFFFFFFF8259E638

    # 0xffffffff82cb3b3a : add rdi, rcx ; ret
    ADD_RDI_RCX_RET = 0xFFFFFFFF82CB3B3A

    # 0xffffffff822bfa87 : sub rsi, rdx ; mov rax, rsi ; pop rbp ; ret
    SUB_RSI_RDX_MOV_RAX_RSI_POP_RBP_RET = 0xFFFFFFFF822BFA87

    # 0xffffffff8280346f : jmp r14
    JMP_R14 = 0xFFFFFFFF8280346F


# FW 10.50 / 10.70 / 10.71
class OffsetsFirmware_1050_1071:
    PPPOE_SOFTC_LIST = 0xFFFFFFFF844514B8

    KERNEL_MAP = 0xFFFFFFFF844A9250

    SETIDT = 0xFFFFFFFF82341470

    KMEM_ALLOC = 0xFFFFFFFF82628960
    KMEM_ALLOC_PATCH1 = 0xFFFFFFFF82628A2C
    KMEM_ALLOC_PATCH2 = 0xFFFFFFFF82628A34

    MEMCPY = 0xFFFFFFFF822D7370

    MOV_CR0_RSI_UD2_MOV_EAX_1_RET = 0xFFFFFFFF82285F39

    SECOND_GADGET_OFF = 0x3B

    # 0xffffffff8221cb8d : jmp qword ptr [rsi + 0x3b]
    FIRST_GADGET = 0xFFFFFFFF8221CB8D

    # 0xffffffff82c74cd6 : push rbp ; jmp qword ptr [rsi]
    PUSH_RBP_JMP_QWORD_PTR_RSI = 0xFFFFFFFF82C74CD6

    # 0xffffffff824a4981 : pop rbx ; pop r14 ; pop rbp ; jmp qword ptr [rsi + 0x10]
    POP_RBX_POP_R14_POP_RBP_JMP_QWORD_PTR_RSI_10 = 0xFFFFFFFF824A4981

    # 0xffffffff82921206 : lea rsp, [rsi + 0x20] ; repz ret
    LEA_RSP_RSI_20_REPZ_RET = 0xFFFFFFFF82921206

    # 0xffffffff826c493a : add rsp, 0x28 ; pop rbp ; ret
    ADD_RSP_28_POP_RBP_RET = 0xFFFFFFFF826C493A

    # 0xffffffff822ce1af : add rsp, 0xb0 ; pop rbp ; ret
    ADD_RSP_B0_POP_RBP_RET = 0xFFFFFFFF822CE1AF

    # 0xffffffff822008e0 : ret
    RET = 0xFFFFFFFF822008E0

    # 0xffffffff8236f38f : pop rdi ; ret
    POP_RDI_RET = 0xFFFFFFFF8236F38F

    # 0xffffffff82222d59 : pop rsi ; ret
    POP_RSI_RET = 0xFFFFFFFF82222D59

    # 0xffffffff82329bb2 : pop rdx ; ret
    POP_RDX_RET = 0xFFFFFFFF82329BB2

    # 0xffffffff8225a567 : pop rcx ; ret
    POP_RCX_RET = 0xFFFFFFFF8225A567

    # 0xffffffff822234fd : pop r8 ; pop rbp ; ret
    POP_R8_POP_RBP_RET = 0xFFFFFFFF822234FD

    # 0xffffffff827aa3ef : pop r12 ; ret
    POP_R12_RET = 0xFFFFFFFF827AA3EF

    # 0xffffffff82495c08 : pop rax ; ret
    POP_RAX_RET = 0xFFFFFFFF82495C08

    # 0xffffffff822008df : pop rbp ; ret
    POP_RBP_RET = 0xFFFFFFFF822008DF

    # 0xffffffff82bb5092 : push rsp ; pop rsi ; ret
    PUSH_RSP_POP_RSI_RET = 0xFFFFFFFF82BB5092

    # 0xffffffff8256d4d0 : mov rdi, qword ptr [rdi] ; pop rbp ; jmp rax
    MOV_RDI_QWORD_PTR_RDI_POP_RBP_JMP_RAX = 0xFFFFFFFF8256D4D0

    # 0xffffffff822a9078 : mov byte ptr [rcx], al ; ret
    MOV_BYTE_PTR_RCX_AL_RET = 0xFFFFFFFF822A9078

    # 0xffffffff8229113c : mov rdi, rbx ; call r12
    MOV_RDI_RBX_CALL_R12 = 0xFFFFFFFF8229113C

    # 0xffffffff82290f77 : mov rdi, r14 ; call r12
    MOV_RDI_R14_CALL_R12 = 0xFFFFFFFF82290F77

    # 0xffffffff8227e3ce : mov rsi, rbx ; call rax
    MOV_RSI_RBX_CALL_RAX = 0xFFFFFFFF8227E3CE

    # 0xffffffff824f95e8 : mov r14, rax ; call r8
    MOV_R14_RAX_CALL_R8 = 0xFFFFFFFF824F95E8

    # 0xffffffff82cb4eca : add rdi, rcx ; ret
    ADD_RDI_RCX_RET = 0xFFFFFFFF82CB4ECA

    # 0xffffffff8220c1e7 : sub rsi, rdx ; mov rax, rsi ; pop rbp ; ret
    SUB_RSI_RDX_MOV_RAX_RSI_POP_RBP_RET = 0xFFFFFFFF8220C1E7

    # 0xffffffff82b83a5b : jmp r14
    JMP_R14 = 0xFFFFFFFF82B83A5B


# FW 11.00
class OffsetsFirmware_1100:
    PPPOE_SOFTC_LIST = 0xFFFFFFFF844E2578

    KERNEL_MAP = 0xFFFFFFFF843FF130

    SETIDT = 0xFFFFFFFF8245BDB0

    KMEM_ALLOC = 0xFFFFFFFF82445E10
    KMEM_ALLOC_PATCH1 = 0xFFFFFFFF82445EDC
    KMEM_ALLOC_PATCH2 = 0xFFFFFFFF82445EE4

    MEMCPY = 0xFFFFFFFF824DDDF0

    # 0xffffffff824f1299 : mov cr0, rsi ; ud2 ; mov eax, 1 ; ret
    MOV_CR0_RSI_UD2_MOV_EAX_1_RET = 0xFFFFFFFF824F1299

    SECOND_GADGET_OFF = 0x3E

    # 0xffffffff82eb1f97 : jmp qword ptr [rsi + 0x3e]
    FIRST_GADGET = 0xFFFFFFFF82EB1F97

    # 0xffffffff82c75166 : push rbp ; jmp qword ptr [rsi]
    PUSH_RBP_JMP_QWORD_PTR_RSI = 0xFFFFFFFF82C75166

    # 0xffffffff824b90e1 : pop rbx ; pop r14 ; pop rbp ; jmp qword ptr [rsi + 0x10]
    POP_RBX_POP_R14_POP_RBP_JMP_QWORD_PTR_RSI_10 = 0xFFFFFFFF824B90E1

    # 0xffffffff8293c8c6 : lea rsp, [rsi + 0x20] ; repz ret
    LEA_RSP_RSI_20_REPZ_RET = 0xFFFFFFFF8293C8C6

    # 0xffffffff826cb2da : add rsp, 0x28 ; pop rbp ; ret
    ADD_RSP_28_POP_RBP_RET = 0xFFFFFFFF826CB2DA

    # 0xffffffff824cdd5f : add rsp, 0xb0 ; pop rbp ; ret
    ADD_RSP_B0_POP_RBP_RET = 0xFFFFFFFF824CDD5F

    # 0xffffffff822007e4 : ret
    RET = 0xFFFFFFFF822007E4

    # 0xffffffff825f38ed : pop rdi ; ret
    POP_RDI_RET = 0xFFFFFFFF825F38ED

    # 0xffffffff8224a6a9 : pop rsi ; ret
    POP_RSI_RET = 0xFFFFFFFF8224A6A9

    # 0xffffffff822a4762 : pop rdx ; ret
    POP_RDX_RET = 0xFFFFFFFF822A4762

    # 0xffffffff8221170a : pop rcx ; ret
    POP_RCX_RET = 0xFFFFFFFF8221170A

    # 0xffffffff8224ae4d : pop r8 ; pop rbp ; ret
    POP_R8_POP_RBP_RET = 0xFFFFFFFF8224AE4D

    # 0xffffffff8279faaf : pop r12 ; ret
    POP_R12_RET = 0xFFFFFFFF8279FAAF

    # 0xffffffff8221172e : pop rax ; ret
    POP_RAX_RET = 0xFFFFFFFF8221172E

    # 0xffffffff822008df : pop rbp ; ret
    POP_RBP_RET = 0xFFFFFFFF822008DF

    # 0xffffffff82bb5c7a : push rsp ; pop rsi ; ret
    PUSH_RSP_POP_RSI_RET = 0xFFFFFFFF82BB5C7A

    # 0xffffffff823ce260 : mov rdi, qword ptr [rdi] ; pop rbp ; jmp rax
    MOV_RDI_QWORD_PTR_RDI_POP_RBP_JMP_RAX = 0xFFFFFFFF823CE260

    # 0xffffffff8236ae58 : mov byte ptr [rcx], al ; ret
    MOV_BYTE_PTR_RCX_AL_RET = 0xFFFFFFFF8236AE58

    # 0xffffffff8233426c : mov rdi, rbx ; call r12
    MOV_RDI_RBX_CALL_R12 = 0xFFFFFFFF8233426C

    # 0xffffffff823340a7 : mov rdi, r14 ; call r12
    MOV_RDI_R14_CALL_R12 = 0xFFFFFFFF823340A7

    # 0xffffffff82512dce : mov rsi, rbx ; call rax
    MOV_RSI_RBX_CALL_RAX = 0xFFFFFFFF82512DCE

    # 0xffffffff82624df8 : mov r14, rax ; call r8
    MOV_R14_RAX_CALL_R8 = 0xFFFFFFFF82624DF8

    # 0xffffffff82cb535a : add rdi, rcx ; ret
    ADD_RDI_RCX_RET = 0xFFFFFFFF82CB535A

    # 0xffffffff8260f297 : sub rsi, rdx ; mov rax, rsi ; pop rbp ; ret
    SUB_RSI_RDX_MOV_RAX_RSI_POP_RBP_RET = 0xFFFFFFFF8260F297

    # 0xffffffff82b84657 : jmp r14
    JMP_R14 = 0xFFFFFFFF82B84657
